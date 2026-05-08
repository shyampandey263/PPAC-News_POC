# PPAC POC - News Fetcher and WhatsApp Notifier

A Python-based application that fetches news from RSS feeds, summarizes articles using OpenAI, and sends notifications via WhatsApp.

## Project Structure

- **app.py** - Main application entry point
- **database.py** - Database models and initialization using SQLAlchemy
- **news_fetcher.py** - RSS feed fetching logic
- **summarizer.py** - Article summarization using OpenAI API
- **whatsapp.py** - WhatsApp message sending via Twilio
- **requirements.txt** - Python dependencies
- **.env** - Environment variables configuration

## Setup Instructions

### 1. Prerequisites

- Python 3.14+ installed
- pip package manager

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit `.env` file with your credentials:

```
OPENAI_API_KEY=your_openai_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890
DATABASE_URL=sqlite:///news.db
NEWS_FETCH_INTERVAL=3600
```

### 4. Run the Application

```bash
python app.py
```

## Features

- **News Fetching**: Automatically fetches news from BBC, The Guardian, and Reuters
- **Article Summarization**: Uses OpenAI's GPT-3.5-turbo to generate concise summaries
- **WhatsApp Integration**: Sends formatted news articles via WhatsApp using Twilio
- **Database Storage**: Persists articles and tracks delivery status
- **Scheduled Fetching**: Configurable fetch intervals

## API Keys Required

1. **OpenAI API Key**: Get from https://platform.openai.com/api-keys
2. **Twilio Credentials**: Get from https://www.twilio.com/console
3. **WhatsApp Business Account**: Required for Twilio WhatsApp integration

## Database Schema

### NewsArticle
- id, title, url (unique), summary, source, published_date, created_at, sent_via_whatsapp

### UserPreference
- id, phone_number (unique), categories, created_at

## Dependencies

- **python-dotenv**: Environment variable management
- **requests**: HTTP library
- **feedparser**: RSS feed parsing
- **openai**: OpenAI API client
- **twilio**: WhatsApp messaging
- **sqlalchemy**: ORM and database toolkit

---

For questions or issues, please refer to the respective API documentation.
