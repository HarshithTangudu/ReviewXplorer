# Testing

## Backend
- Currently, there is a lack of formal unit testing or integration testing frameworks (like `pytest`).
- **Manual Scripts:** Debugging and manual ad-hoc testing are done via `debug_all.py` and `debug_amazon.py` found in the root backend directory. These are used to manually trigger scrapers to test stability.

## Frontend
- No automated test suite (like Jest, Vitest, or Cypress) is visible in the frontend codebase. Everything relies on manual browser testing and React Fast Refresh provided by Vite.
