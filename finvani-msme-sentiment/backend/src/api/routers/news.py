from fastapi import APIRouter, HTTPException, BackgroundTasks
import json
import os
from pathlib import Path
from typing import List, Dict, Any
import logging
from src.ingestion.rss_google_news import GoogleNewsIngester, LANGUAGES

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/news",
    tags=["news"]
)

def get_data_dir() -> Path:
    # Resolve path relative to this file
    current_dir = Path(__file__).resolve().parent
    # Go up to project root
    project_root = current_dir.parent.parent.parent.parent
    return project_root / "data" / "raw"

def get_latest_data_file() -> Path | None:
    data_dir = get_data_dir()
    
    if not data_dir.exists():
        logger.warning(f"Data directory not found: {data_dir}")
        return None
        
    files = list(data_dir.glob("*.jsonl"))
    if not files:
        return None
        
    # Sort by filename (YYYY-MM-DD.jsonl) descending
    files.sort(key=lambda x: x.name, reverse=True)
    return files[0]

def run_ingestion_task():
    logger.info("Starting background ingestion task...")
    try:
        data_dir = get_data_dir()
        ingester = GoogleNewsIngester(str(data_dir))
        queries = ["MSME", "SME India", "Business Loan", "Economy"]
        ingester.run_ingestion(queries, LANGUAGES)
        logger.info("Background ingestion task completed.")
    except Exception as e:
        logger.error(f"Background ingestion failed: {e}")

@router.get("/status")
async def get_ingestion_status():
    """Debug endpoint to check if data files exist."""
    data_dir = get_data_dir()
    if not data_dir.exists():
        return {"status": "error", "message": "Data directory does not exist", "files": []}
    
    files = list(data_dir.glob("*.jsonl"))
    file_info = [{"name": f.name, "size": f.stat().st_size, "modified": f.stat().st_mtime} for f in files]
    return {
        "status": "ok",
        "count": len(files),
        "files": file_info,
        "path": str(data_dir)
    }

@router.post("/refresh")
async def refresh_news(background_tasks: BackgroundTasks):
    """Trigger a fresh fetch of news from Google RSS."""
    background_tasks.add_task(run_ingestion_task)
    return {"message": "Ingestion started in background. Please wait a few moments and refresh."}

import random

@router.get("/latest", response_model=List[Dict[str, Any]])
async def get_latest_news(lang: str = None, randomize: bool = False):
    latest_file = get_latest_data_file()
    
    if not latest_file:
        return [
            {
                "title": "No data found - please run ingestion script",
                "link": "#",
                "published_date": "N/A",
                "source": "System",
                "language": "en"
            }
        ]
    
    articles = []
    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    article = json.loads(line)
                    # Filter by language if provided (and if article has language field)
                    if lang and article.get("language") != lang:
                        continue
                        
                    articles.append(article)
                except json.JSONDecodeError:
                    continue
                
                # If randomize is False, we can break early optimization
                # But if randomize is True, we need a larger pool to sample from
                if not randomize and len(articles) >= 50:
                    break
                # Only cap at a larger number if randomizing
                if randomize and len(articles) >= 200:
                    break
                    
        # Apply randomization if requested
        if randomize and articles:
            random.shuffle(articles)
            
        # Return top 50
        return articles[:50]
        
    except Exception as e:
        logger.error(f"Error reading data file: {e}")
        raise HTTPException(status_code=500, detail="Error processing news data")
