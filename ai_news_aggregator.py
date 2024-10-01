# app.py
__version__ = "1.1.0.0"

import os
import asyncio
import aiohttp
from newsapi import NewsApiClient
import logging
from openai import AsyncOpenAI
import gradio as gr
import traceback

# Set up detailed logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve API keys from environment variables
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Check if API keys are available
if not NEWSAPI_KEY or not OPENAI_API_KEY:
    logging.error("API keys are missing. Please check your environment variables.")

# Initialize the AsyncOpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

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

async def summarize_article(article_text):
    """Asynchronously summarize an article using OpenAI's GPT model."""
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional news summarizer. Provide concise, informative summaries."},
                {"role": "user", "content": f"Summarize this news article in 2-3 sentences, highlighting key points: {article_text}"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error summarizing article: {str(e)}")
        logging.error(traceback.format_exc())
        return f"Error generating summary: {str(e)}"

async def process_article(article):
    """Process a single article: extract info and generate summary."""
    try:
        source = article['source']['name']
        title = article.get('title', 'No title available')
        description = article.get('description') or article.get('content') or title
        url = article.get('url', '#')
        image_url = article.get('urlToImage', '')

        summary = await summarize_article(description)

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

async def news_aggregator_async(category):
    """Main asynchronous function to aggregate and summarize news."""
    try:
        logging.info(f"Fetching headlines for category: {category}")
        articles = fetch_global_headlines(category=category)
        
        if not articles:
            return "No news articles found for this category. Please try another category."

        logging.info(f"Found {len(articles)} articles. Processing...")
        
        # Process all articles concurrently
        summarized_articles = await asyncio.gather(
            *[process_article(article) for article in articles],
            return_exceptions=True
        )

        # Filter out any exceptions and log them
        valid_summaries = []
        for result in summarized_articles:
            if isinstance(result, Exception):
                logging.error(f"Error processing an article: {str(result)}")
            else:
                valid_summaries.append(result)

        if not valid_summaries:
            return "Error processing news articles. Please try again later."

        logging.info(f"Successfully processed {len(valid_summaries)} articles")
        return "".join(valid_summaries)
    except Exception as e:
        logging.error(f"Error in news_aggregator_async: {str(e)}")
        logging.error(traceback.format_exc())
        return f"An error occurred: {str(e)}"

def news_aggregator(category):
    """Wrapper function for the Gradio interface."""
    try:
        # Use asyncio.run to ensure the event loop is managed properly
        return asyncio.run(news_aggregator_async(category))
    except Exception as e:
        logging.error(f"Error in news_aggregator: {str(e)}")
        logging.error(traceback.format_exc())
        return f"An error occurred: {str(e)}"


# List of available news categories
CATEGORIES = [
    "business", "entertainment", "general", "health",
    "science", "sports", "technology"
]

# CSS styles for the Gradio interface
css = """
.article-card { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 8px; }
.article-card h3 { margin-top: 0; }
.article-image { max-width: 100%; height: auto; margin-top: 10px; border-radius: 5px; }
"""

# Set up the Gradio interface
iface = gr.Interface(
    fn=news_aggregator,
    inputs=gr.Dropdown(choices=CATEGORIES, label="Select News Category"),
    outputs=gr.HTML(label="AI-Summarized News"),
    title="AI Global News Aggregator",
    description="Get AI-summarized news headlines from various categories.",
    article="This tool uses AI to fetch and summarize current news articles.",
    css=css
)

# Main entry point of the application
if __name__ == "__main__":
    iface.launch()