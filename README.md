---
title: AI Global News Aggregator
emoji: 📰
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.44.1
app_file: app.py
pinned: false
---
# AI Global News Aggregator

## Overview

The `AI Global News Aggregator` is a Python application built using Gradio and leveraging the NewsAPI and OpenAI's GPT-3.5-Turbo models to provide users with AI-generated summaries of global news headlines. This tool allows users to select a news category and receive a list of articles with summaries, sources, and optional images.

## Features

- **News Fetching**: Utilizes the NewsAPI to retrieve top headlines from various categories.
- **Article Summarization**: Uses OpenAI's GPT-3.5-Turbo to generate concise summaries of each article.
- **User Interface**: Provides an interactive web interface using Gradio where users can select a news category and view the summarized news.

## Installation

### Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8+
- Environment variables set for `NEWSAPI_KEY` and `OPENAI_API_KEY`

### Installation Steps

1. Clone the repository or download the code.
2. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Usage

1. Set the necessary environment variables (`NEWSAPI_KEY` and `OPENAI_API_KEY`) in your system.
2. Run the application:

```bash
python app.py
```

This will start the Gradio interface on your local machine, typically accessible at `http://localhost:7860`.

## Code Explanation

### Imports

```python
import os
from newsapi import NewsApiClient
import logging
from openai import OpenAI
import gradio as gr
```

These imports include necessary libraries for interacting with APIs, handling logging, and creating the user interface.

### Environment Variables

```python
NEWSAPI_KEY = os.environ.get('NEWSAPI_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
```

Environment variables are used to store sensitive information such as API keys securely.

### Logging Configuration

```python
logging.basicConfig(level=logging.INFO)
```

Sets up basic configuration for logging to capture informational messages.

### Functions

#### `fetch_global_headlines`

Retrieves top headlines from the NewsAPI based on the specified category.

#### `summarize_article`
Generates a summary of a given article text using the OpenAI GPT-3.5-Turbo model.
#### `news_aggregator`

Aggregates news articles by fetching headlines and summarizing them. It constructs HTML content for display.

### Categories

```python
CATEGORIES = [
    "business", "entertainment", "general", "health",
    "science", "sports", "technology"
]
```

List of predefined news categories.

### Gradio Interface

```python
iface = gr.Interface(
    fn=news_aggregator,
    inputs=gr.Dropdown(choices=CATEGORIES, label="Global News Category"),
    outputs=gr.HTML(label="Global News Summaries"),
    title="AI Global News Aggregator",
    description="Select a category to get AI-summarized global news headlines with links and images."
)
iface.launch()
```

Creates and launches the Gradio interface, allowing users to interact with the application through a web browser.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License 
```

**Current Version**: 1.1.0.0

## Recent Updates (Version 1.1.0.0 - Day 4)

1. **Asynchronous Processing**
   - Implemented asynchronous API calls using `asyncio` and `aiohttp`.
   - Improved overall performance by allowing concurrent processing of multiple articles.
2. **Caching Mechanism**
   - Added caching for article summaries using `lru_cache`.
   - Reduces API calls and improves response time for previously summarized articles.
3. **Enhanced Error Handling**
   - Improved error logging and handling for both NewsAPI and OpenAI API calls.
   - More informative error messages for users in case of API failures.
4. **UI Enhancements**
   - Updated CSS for a more polished look.
   - Improved layout of article cards for better readability.
5. **Performance Optimizations**
   - Reduced latency in fetching and summarizing articles.
   - Improved overall responsiveness of the application.
6. **Prompt Engineering
   - Refined AI prompts to provide more concise, focused, and informative news article summaries.
   - System message added to guide the AI for consistent results.
7. **Testing Improvements
   - Performed iterative testing to ensure that the prompt engineering and async updates provide consistent results across various articles.
   - Focused on maintaining quality, relevance, and performance improvements.
This README provides a comprehensive overview of the application, its features, installation steps, usage instructions, and additional details to help users understand and utilize the `AI Global News Aggregator`.
