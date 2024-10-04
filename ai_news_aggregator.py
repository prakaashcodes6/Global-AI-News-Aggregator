# ai-news.py
__version__ = "1.2.0.0"

import os
import asyncio
import aiohttp
from newsapi import NewsApiClient
import logging
from openai import AsyncOpenAI
import gradio as gr
import traceback
from collections import OrderedDict

# Set up detailed logging for debugging purposes
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve API keys from environment variables
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Check if API keys are available
if not NEWSAPI_KEY or not OPENAI_API_KEY:
    logging.error("API keys are missing. Please check your environment variables.")

# Initialize the AsyncOpenAI client with your API key
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Simple cache implementation
class SimpleCache:
    def __init__(self, max_size=100):
        self.cache = OrderedDict()
        self.max_size = max_size

    async def get(self, key, create_func):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        
        value = await create_func()
        self.cache[key] = value
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
        return value

# Initialize the cache
summary_cache = SimpleCache(max_size=100)

def fetch_global_headlines(category='general', page_size=10):
    """Fetch news headlines from NewsAPI."""
    try:
        newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
        top_headlines = newsapi.get_top_headlines(
            category=category,
            language='en',
            page_size=page_size
        )
        logging.info(f"NewsAPI Response: {len(top_headlines['articles'])} articles fetched")
        return top_headlines['articles']
    except Exception as e:
        logging.error(f"Error fetching headlines: {str(e)}")
        logging.error(traceback.format_exc())
        return []

async def warm_up_openai():
    """Send a dummy request to OpenAI to warm up the connection."""
    try:
        await client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Warm-up request"}],
            max_tokens=5
        )
        logging.info("OpenAI connection warmed up successfully.")
    except Exception as e:
        logging.error(f"Error warming up OpenAI connection: {str(e)}")
        logging.error(traceback.format_exc())

async def translate_text(text: str, target_language: str) -> str:
    """Translate the given text to the target language using GPT-4."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the following text to {target_language}."},
                {"role": "user", "content": text}
            ],
            max_tokens=250,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error translating text: {str(e)}")
        return text  # Return original text if translation fails

async def summarize_article(article_text: str, language: str) -> str:
    """Asynchronously summarize an article using OpenAI's GPT-4 model and translate if needed."""
    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert news analyst and summarizer. Provide concise, insightful summaries that capture the core of news articles, including key events, figures, and implications."},
                {"role": "user", "content": f"Summarize this news article in 2-3 sentences. Highlight the main event, key figures, and any significant impacts or outcomes. Ensure the summary is informative and contextual. Article: {article_text[:1000]}"}
            ],
            max_tokens=150,
            temperature=0.5
        )
        summary = response.choices[0].message.content.strip()
        
        if language.lower() != "english":
            summary = await translate_text(summary, language)
        
        return summary
    except Exception as e:
        logging.error(f"Error summarizing article: {str(e)}")
        logging.error(traceback.format_exc())
        return "Unable to generate summary due to an error. Please refer to the original article for information."

async def process_article(article, language):
    """Process a single article: extract info, generate summary, and translate title if needed."""
    try:
        source = article.get('source', {}).get('name', '[Source Unavailable]')
        title = article.get('title', '[Title Unavailable]')
        description = article.get('description') or article.get('content') or title
        url = article.get('url', '#')
        image_url = article.get('urlToImage', '')

        if not title or not description or len(description) < 50:
            logging.warning(f"Skipping article due to insufficient content: {title}")
            return f"""
            <div class='article-card'>
                <h3><a href='{url}' target='_blank'>{title or '[Title Unavailable]'}</a></h3>
                <p><strong>Source:</strong> {source or '[Source Unavailable]'}</p>
                <p><strong>Summary:</strong> Content unavailable for this article.</p>
            </div>
            """

        cache_key = f"{description[:1000]}_{language}"
        summary = await summary_cache.get(cache_key, lambda: summarize_article(description, language))
        
        if len(summary) < 50:
            summary = f"Summary unavailable. Please read the full article at: {url}"

        # Translate the title if the language is not English
        if language.lower() != "english":
            title = await translate_text(title, language)

        return f"""
        <div class='article-card'>
            <h3><a href='{url}' target='_blank'>{title}</a></h3>
            <p><strong>Source:</strong> {source}</p>
            <p><strong>Summary:</strong> {summary}</p>
            {f'<img src="{image_url}" alt="Article image" class="article-image">' if image_url else ''}
        </div>
        """
    except Exception as e:
        logging.error(f"Error processing article: {str(e)}")
        logging.error(traceback.format_exc())
        return f"<div>Error processing article: {str(e)}</div>"

async def news_aggregator_async(category, language):
    """Main asynchronous function to aggregate and summarize news."""
    try:
        await warm_up_openai()

        logging.info(f"Fetching headlines for category: {category}")
        articles = fetch_global_headlines(category=category)
        
        if not articles:
            return "No news articles found for this category. Please try another category."

        logging.info(f"Found {len(articles)} articles. Processing...")

        tasks = [process_article(article, language) for article in articles]
        summarized_articles = await asyncio.gather(*tasks)

        if not summarized_articles:
            return "Error processing news articles. Please try again later."

        logging.info(f"Successfully processed {len(summarized_articles)} articles")
        return "".join(summarized_articles)
    except Exception as e:
        logging.error(f"Error in news_aggregator_async: {str(e)}")
        logging.error(traceback.format_exc())
        return "We're experiencing technical difficulties. Please try again later or choose a different category."

def news_aggregator(category, language):
    """Wrapper function for the Gradio interface."""
    if not category or not language:
        return "Please select a news category and language."
    try:
        return asyncio.run(news_aggregator_async(category, language))
    except Exception as e:
        logging.error(f"Error in news_aggregator: {str(e)}")
        logging.error(traceback.format_exc())
        return f"An error occurred: {str(e)}"

# List of available news categories
CATEGORIES = [
    "business", "entertainment", "general", "health",
    "science", "sports", "technology"
]

# List of supported languages
LANGUAGES = ["English", "Spanish", "French", "German", "Chinese", "Hindi", "Arabic"]

# CSS styles for the Gradio interface
css = """
.article-card { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 8px; }
.article-card h3 { margin-top: 0; }
.article-image { max-width: 100%; height: auto; margin-top: 10px; border-radius: 5px; }
"""

# Set up the Gradio interface with a custom layout
with gr.Blocks(css=css) as iface:
    gr.Markdown("# AI Global News Aggregator")
    gr.Markdown("Get AI-summarized news headlines from various categories in multiple languages.")
    
    with gr.Row():
        with gr.Column(scale=1):
            category_input = gr.Dropdown(choices=CATEGORIES, label="Select News Category")
            language_input = gr.Dropdown(choices=LANGUAGES, label="Select Language", value="English")
            submit_button = gr.Button("Get News Summaries")
        
        with gr.Column(scale=2):
            output = gr.HTML(label="AI-Summarized News")
    
    submit_button.click(fn=news_aggregator, inputs=[category_input, language_input], outputs=output)

    gr.Examples(
        examples=[["business", "English"], ["technology", "Spanish"], ["sports", "French"], 
                  ["health", "Hindi"], ["science", "Arabic"]],
        inputs=[category_input, language_input],
        outputs=output,
        fn=news_aggregator,
        cache_examples=True,
    )

    gr.Markdown("This tool uses AI to fetch, summarize, and translate current news articles.")

# Main entry point of the application
if __name__ == "__main__":
    iface.launch()
