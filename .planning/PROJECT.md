# ReviewXplorer

## What This Is

ReviewXplorer is a full-stack web application that allows users to paste URLs from Amazon, Flipkart, YouTube, or Reddit. It scrapes the reviews and comments and performs advanced sentiment, emotion, and sarcasm analysis (using BERT-based models, transitioning toward LSTM if required) to provide rich data visualizations.

## Core Value

To provide instant, deep insights into user reviews and comments across multiple platforms through an interactive and visually appealing dashboard.

## Requirements

### Validated

- ✓ Cross-platform scraping of comments (Amazon, Flipkart, YouTube, Reddit) — existing
- ✓ NLP analysis for sentiment (positive/negative), emotion, and sarcasm — existing
- ✓ Basic dashboard visualization using Recharts — existing
- ✓ ML model integration via Hugging Face `transformers` — existing

### Active

- [ ] Fix and stabilize Amazon and Flipkart scrapers which are currently broken
- [ ] Implement enhanced, "cooler" visualizations for an improved user experience
- [ ] Evaluate replacing/augmenting existing BERT models with LSTM

### Out of Scope

- [Full integration of a custom trained LSTM model immediately] — Focus first on scraper fixes and UI improvements; keep existing BERT fallback if LSTM proves too resource-heavy to build from scratch quickly.

## Context

- The project relies heavily on Playwright for scraping eCommerce sites (Amazon/Flipkart), which is brittle against UI changes. This is a known issue.
- The UI currently uses a standard Recharts setup, but there is demand for more dynamic/advanced charts and animations to make it "cooler".
- The system heavily queries Hugging Face pipelines concurrently.

## Constraints

- **Scraping**: E-commerce sites update their DOM frequently — scrapers require constant maintenance.
- **ML Models**: Inference is computationally expensive.
- **Timeline**: Scraper fixes are a priority blocker for user experience.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Prioritize scraper fixes first | Without data ingestion, the visualizations cannot be tested or used. | — Pending |
| Add new visualizations on top of existing Recharts | Enhancing the current UI stack is faster than rewriting the entire graphing library. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-09 after initialization*
