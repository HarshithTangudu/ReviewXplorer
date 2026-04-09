# System Architecture

## Overview
ReviewXplorer follows a standard Client-Server architectural pattern, separating the presentation layer (React frontend) from the business logic and data processing layer (FastAPI backend). The core functionality heavily features a multi-threaded data ingestion tier and a machine-learning-powered NLP analysis tier.

## High-Level Components

### 1. Frontend (Client)
- **Single Page Application:** Built with React/Vite.
- **State Management:** Uses React built-in hooks (`useState`, `useMemo`).
- **Functionality:** 
  - Provides a search bar for users to input URLs.
  - Communicates with the backend REST API via Axios.
  - Renders interactive data visualization using Recharts.

### 2. Backend (API Layer)
- **FastAPI Application:** Hosts the API routes, primarily `POST /analyze`.
- **CORS Handling:** Uses `CORSMiddleware` to accept requests from the frontend.
- **Data Schema:** Defines Pydantic models for structured requests (`AnalysisRequest`) and responses (`AnalysisResponse`, `CommentResult`).

### 3. Scraping Tier (`ScraperManager`)
- Orchestrates different scrapers dynamically based on the provided URL.
- Pluggable design where different strategies (Amazon, Flipkart, Reddit, YouTube) are dispatched via a central factory/manager.

### 4. Analysis Tier (`AnalyzerService`)
- Manages heavy ML operations.
- **Pipelines:** Initializes `transformers` pipelines on startup and persists them in memory to avoid reloading for every request.
- Performs inference on scraped textual data (up to 512 tokens max per text), returning sentiment, emotion, and sarcasm likelihood.

## Data Flow
1. User enters a URL on the frontend and clicks "Analyze".
2. Frontend sends `POST http://localhost:8000/analyze` with the payload `{ url: ... }`.
3. Backend identifies the platform (`scraper_manager.get_platform`).
4. The corresponding scraper asynchronously fetches comments from the target URL.
5. `AnalyzerService.analyze()` runs the comments through HF Transformer pipelines.
6. `AnalyzerService.get_summary()` aggregates the ML outputs into distributions.
7. Backend responds with the aggregated data and individual comment results.
8. Frontend renders data graphs and allows pagination/filtering.
