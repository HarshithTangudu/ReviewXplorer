from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from scrapers.manager import ScraperManager
from services.analyzer_service import AnalyzerService

app = FastAPI(title="ReviewXplorer API")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
scraper_manager = ScraperManager()
analyzer_service = AnalyzerService()

class AnalysisRequest(BaseModel):
    url: str

class CommentResult(BaseModel):
    text: str
    sentiment: str
    emotion: str
    sarcastic: bool
    confidence: float

class AnalysisResponse(BaseModel):
    platform: str
    total_comments: int
    results: List[CommentResult]
    summary: dict

@app.get("/")
async def root():
    return {"message": "ReviewXplorer API is running"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_url(request: AnalysisRequest):
    platform = scraper_manager.get_platform(request.url)
    if platform == "Unknown":
        raise HTTPException(status_code=400, detail="Unsupported platform")

    print(f"Scraping {platform} at {request.url}...")
    comments = await scraper_manager.scrape(request.url)
    
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found or platform not reachable")
    
    print(f"Found {len(comments)} comments. Analyzing...")
    results = analyzer_service.analyze(comments)
    summary = analyzer_service.get_summary(results)
    
    return {
        "platform": platform,
        "total_comments": len(results),
        "results": results,
        "summary": summary
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
