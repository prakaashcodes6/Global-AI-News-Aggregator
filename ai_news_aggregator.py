# news_aggregator.py

# Import API keys from config
from config import NEWSAPI_KEY, OPENAI_API_KEY

from newsapi import NewsApiClient
import logging
from openai import OpenAI
import gradio as gr

logging.basicConfig(level=logging.INFO)

def fetch_global_headlines(category='general', page_size=10):
    try:
        newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
        top_headlines = newsapi.get_top_headlines(category=category,
                                                  language='en',
                                                  page_size=page_size)
        if not top_headlines['articles']:
            logging.warning(f"No articles found for category: {category}")
        return top_headlines['articles']
    except Exception as e:
        logging.error(f"Error fetching headlines: {str(e)}")
        return []

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_article(article_text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
                {"role": "user", "content": f"Summarize this news article in 2-3 sentences: {article_text}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error summarizing article: {str(e)}")
        return "Error generating summary."

def news_aggregator(category):
    articles = fetch_global_headlines(category=category)
    if not articles:
        return "No news articles found for this category. Please try another category."
    
    summarized_articles = []
    for article in articles:
        try:
            source = article['source']['name']
            title = article.get('title', 'No title available')
            description = article.get('description') or article.get('content') or title
            summary = summarize_article(description)
            url = article.get('url', '#')
            image_url = article.get('urlToImage', '')
            
            article_html = f"""
            <div style='margin-bottom: 20px; border: 1px solid #ddd; padding: 10px; border-radius: 5px;'>
                <h3><a href='{url}' target='_blank'>{title}</a></h3>
                <p><strong>Source:</strong> {source}</p>
                <p><strong>Summary:</strong> {summary}</p>
                {f'<img src="{image_url}" style="max-width:100%; height:auto; margin-top:10px;">' if image_url else ''}
            </div>
            """
            summarized_articles.append(article_html)
        except Exception as e:
            logging.error(f"Error processing article: {str(e)}")
    
    if not summarized_articles:
        return "Error processing news articles. Please try again later."
    
    return "".join(summarized_articles)

CATEGORIES = [
    "business", "entertainment", "general", "health",
    "science", "sports", "technology"
]

iface = gr.Interface(
    fn=news_aggregator,
    inputs=gr.Dropdown(choices=CATEGORIES, label="Global News Category"),
    outputs=gr.HTML(label="Global News Summaries"),
    title="AI Global News Aggregator",
    description="Select a category to get AI-summarized global news headlines with links and images."
)

if __name__ == "__main__":
    iface.launch(debug=True, share=True)