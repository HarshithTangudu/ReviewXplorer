# Roadmap: ReviewXplorer

## Overview

The journey from the current prototype to version 1.1 with stable data ingestion and an enhanced visual UX.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Stabilize Scraping Architecture** - Fix Amazon and Flipkart scrapers against anti-bot/DOM changes (completed 2026-04-09)
- [ ] **Phase 2: Modernize Data Visualizations** - Implement interactive and animated visual charts

## Phase Details

### Phase 1: Stabilize Scraping Architecture
**Goal**: Restore data ingestion capabilities for the primary eCommerce platforms.
**Depends on**: Nothing
**Requirements**: [SCRP-01, SCRP-02, SCRP-03]
**Success Criteria** (what must be TRUE):
  1. User can successfully scrape Amazon product reviews without bot blocking/errors.
  2. User can successfully scrape Flipkart product reviews without errors.
  3. Errors from missing URLs or blocked pages are displayed gracefully to the user.
**Plans**: 1 plan

Plans:
- [x] 01-01: Migrate Scrapers to Async Playwright

### Phase 2: Modernize Data Visualizations
**Goal**: Elevate the user experience by building dynamic, "cooler" charts.
**Depends on**: Phase 1
**Requirements**: [VIS-01, VIS-02, VIS-03]
**Success Criteria** (what must be TRUE):
  1. Sentiment timeline/gauge chart is available and functional.
  2. Emotion breakdown provides tooltip-driven interactivity.
  3. Loading new data triggers fluid animations.
**Plans**: 2 plans

Plans:
- [ ] 02-01: Recharts Emotion Breakdown & Contextual Tooltips
- [ ] 02-02: Gauge & Animated Timeline for Sentiment

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Stabilize Scraping Architecture | 1/1 | Complete   | 2026-04-09 |
| 2. Modernize Data Visualizations | 0/2 | Not started | - |
