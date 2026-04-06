# ReviewXplorer

ReviewXplorer is a full-stack web application that performs advanced sentiment, emotion, and sarcasm analysis on comments scraped from Amazon, Flipkart, YouTube, and Reddit.

## Features
- **Multi-Platform Scraping:** Supports Amazon, Flipkart, YouTube, and Reddit.
- **Advanced NLP:** Uses BERT for Emotion & Sarcasm detection and a Sentiment engine.
- **Interactive Dashboard:** Visualizes results using Recharts.
- **Modern UI:** Clean, responsive design with Lucide icons.

## Tech Stack
- **Frontend:** React, TypeScript, Vite, Recharts, Lucide-React.
- **Backend:** FastAPI, Playwright, Transformers (Hugging Face), PRAW.

## Setup Instructions

### Backend
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Install Playwright browsers:
   ```bash
   python -m playwright install chromium
   ```
4. (Optional) Create a `.env` file for Reddit API:
   ```env
   REDDIT_CLIENT_ID=your_id
   REDDIT_CLIENT_SECRET=your_secret
   ```
5. Run the server:
   ```bash
   python main.py
   ```

### Frontend
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## How to Use
1. Paste a product or post link from a supported platform.
2. Click **Analyze**.
3. View the sentiment breakdown, emotion distribution, and sarcasm stats.
