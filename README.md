AI Global News Aggregator
Project Overview
The AI Global News Aggregator is a Python-based application that fetches global news headlines from various categories, uses AI to generate concise summaries, and presents them through an interactive web interface. This project combines the power of NewsAPI for content retrieval and OpenAI's GPT model for intelligent summarization.
Features

Fetch top news headlines from multiple categories
AI-powered summarization of news articles
Interactive web interface for easy news browsing
Support for various news categories (business, entertainment, general, health, science, sports, technology)
Display of original article links and images

Technologies Used

Python 3.7+
NewsAPI for fetching news articles
OpenAI GPT-3.5-turbo for AI summarization
Gradio for creating the web interface
Logging for error handling and debugging

Installation

Clone the repository:
Copygit clone https://github.com/prakaashcodes6/Global-AI-News-Aggregator.git
cd Global-AI-News-Aggregator

Install required packages:
Copypip install -r requirements.txt

Set up API keys:

Rename config_template.py to config.py
Add your NewsAPI and OpenAI API keys to config.py



Configuration
In config.py, add your API keys:
pythonCopyNEWSAPI_KEY = "your_newsapi_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
Ensure config.py is listed in .gitignore to keep your API keys secure.
Usage
Run the application:
Copypython news_aggregator.py
The Gradio interface will launch, providing a URL to access the web interface. Select a news category from the dropdown to fetch and summarize the latest news articles.
Features in Detail

Global News Fetching: Utilizes NewsAPI to retrieve top headlines from various categories.
AI Summarization: Employs OpenAI's GPT-3.5-turbo model to generate concise summaries of news articles.
Category-based Filtering: Allows users to select from predefined news categories.
Error Handling: Implements logging for tracking errors and debugging.
Responsive Design: Presents news articles with titles, sources, summaries, and images in a clean, readable format.

Code Structure

fetch_global_headlines(): Retrieves news articles from NewsAPI.
summarize_article(): Uses OpenAI's API to summarize article content.
news_aggregator(): Main function that combines fetching and summarization.
Gradio interface setup for user interaction.

Customization

Modify the CATEGORIES list to add or remove news categories.
Adjust the page_size parameter in fetch_global_headlines() to change the number of articles fetched.
Edit the summarization prompt in summarize_article() to alter the AI's summarization style.

Future Enhancements

Implement user authentication for personalized news feeds
Add support for multiple languages
Incorporate sentiment analysis of news articles
Develop a feature for saving favorite articles

Contributing
Contributions to improve the AI Global News Aggregator are welcome. Please feel free to submit pull requests or create issues for bugs and feature requests.

License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Acknowledgments

NewsAPI for providing access to global news sources
OpenAI for their powerful GPT model
Gradio for simplifying the creation of web interfaces for ML models
