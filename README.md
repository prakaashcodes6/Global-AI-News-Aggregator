AI Global News Aggregator
🌐 Overview
AI Global News Aggregator is an advanced tool that fetches, summarizes, and translates news articles from various categories using artificial intelligence. It leverages the power of GPT-4 to provide concise, insightful summaries of news articles in multiple languages, making it easier for users to stay informed about global events.
✨ Features

📰 Fetches latest news articles from various categories using NewsAPI
🤖 Utilizes OpenAI's GPT-4 for high-quality article summarization
🌍 Supports multiple languages for summaries and translations
🔄 Implements asynchronous processing for improved performance
💾 Utilizes a caching mechanism for efficient data retrieval
🖥️ Provides a user-friendly interface built with Gradio

🚀 Getting Started
Prerequisites

Python 3.7+
NewsAPI Key
OpenAI API Key

Installation

Clone the repository:
Copygit clone https://github.com/prakaashcodes6/Global-AI-News-Aggregator.git
cd Global-AI-News-Aggregator

Install required dependencies:
Copypip install -r requirements.txt

Set up environment variables:

Create a .env file in the project root
Add your API keys:
CopyNEWSAPI_KEY=your_newsapi_key_here
OPENAI_API_KEY=your_openai_api_key_here


💻 Usage
Run the application:
Copypython main.py
The Gradio interface will launch, allowing you to:

Select a news category
Choose a language for the summaries
Click "Get News Summaries" to fetch and process articles

🛠 Technical Details
Components

NewsAPI Integration: Fetches current news articles from various categories.
OpenAI GPT-4: Provides AI-powered summarization and translation.
Asynchronous Processing: Utilizes asyncio for efficient article processing.
Caching Mechanism: Implements a simple cache to store and retrieve summaries.
Gradio Interface: Offers an intuitive user interface for interaction.

Key Functions

fetch_global_headlines(): Retrieves news articles from NewsAPI.
summarize_article(): Generates concise summaries using GPT-4.
translate_text(): Translates text to the specified language.
process_article(): Handles the entire article processing pipeline.
news_aggregator_async(): Main asynchronous function orchestrating the entire process.

🔧 Configuration

Modify CATEGORIES list to add or remove news categories.
Adjust LANGUAGES list to change available language options.
Customize the Gradio interface in the gr.Blocks() section for different layouts or features.

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgements

NewsAPI for providing access to global news articles.
OpenAI for the powerful GPT-4 model.
Gradio for the intuitive interface building tools.

📞 Contact
For any queries or suggestions, please open an issue in the GitHub repository.

Developed with ❤️ by [Prakaash](https://github.com/prakaashcodes6)