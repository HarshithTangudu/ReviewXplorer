# Directory Structure

## Root
- `README.md`: Basic setup and feature overview documentation.
- `.gitignore`: Common git ignores.

## `frontend/`
- `package.json`, `package-lock.json`: NPM dependencies.
- `vite.config.ts`, `tsconfig.*.json`, `eslint.config.js`: Build and lint configurations.
- `index.html`: Entry HTML file.
- `src/`: Main source files for React.
  - `App.tsx`: Component housing the entire UI logic including search, API calls, and displaying charts.
  - `main.tsx`: React DOM bootstrapping.
  - `App.css`, `index.css`: Styling files embodying the dark/glassmorphic theme.

## `backend/`
- `main.py`: Entry point for the FastAPI server. Defines API endpoints.
- `requirements.txt`: Python package dependencies.
- `debug_all.py`, `debug_amazon.py`: Scripts likely used for manual scraper testing and debugging.
- `scrapers/`: Module responsible for data ingestion.
  - `manager.py`: Coordinator identifying URLs and routing to appropriate scraper.
  - `base.py`: Likely an interface or base class for scrapers.
  - `amazon.py`, `flipkart.py`, `reddit.py`, `youtube.py`: Platform-specific scraping implementations.
- `services/`: Core logic and integration with ML models.
  - `analyzer_service.py`: Encapsulates Hugging Face NLP model loading and inference logic.
