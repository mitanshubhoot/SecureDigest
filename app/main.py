import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Daily Risk Digest")

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
DIGESTS_DIR = BASE_DIR / "digests"
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def load_index() -> list:
    """Load the digest index file."""
    index_file = DIGESTS_DIR / "index.json"
    if not index_file.exists():
        return []
    try:
        with open(index_file, "r") as f:
            return json.load(f)
    except Exception:
        return []


def load_digest(date: str) -> Optional[dict]:
    """Load a specific digest by date."""
    digest_file = DIGESTS_DIR / f"{date}.json"
    if not digest_file.exists():
        return None
    try:
        with open(digest_file, "r") as f:
            return json.load(f)
    except Exception:
        return None


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    """Homepage showing latest digest and past digests list."""
    index = load_index()
    
    # Get latest digest
    latest_digest = None
    if index:
        latest_date = index[0]
        latest_digest = load_digest(latest_date)
    
    # Get last 30 digests
    past_digests = []
    for date in index[:30]:
        digest = load_digest(date)
        if digest:
            past_digests.append({
                "date": date,
                "headline": digest.get("headline", "")
            })
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "latest_digest": latest_digest,
            "past_digests": past_digests,
            "has_digests": len(past_digests) > 0
        }
    )


@app.get("/digest/{date}", response_class=HTMLResponse)
async def view_digest(request: Request, date: str):
    """View a specific digest by date."""
    digest = load_digest(date)
    if not digest:
        raise HTTPException(status_code=404, detail="Digest not found")
    
    return templates.TemplateResponse(
        "digest.html",
        {
            "request": request,
            "digest": digest
        }
    )


@app.get("/api/digests")
async def api_digests():
    """API endpoint returning list of all digest dates."""
    index = load_index()
    return JSONResponse(content=index)


@app.get("/api/digest/{date}")
async def api_digest(date: str):
    """API endpoint returning a specific digest."""
    digest = load_digest(date)
    if not digest:
        raise HTTPException(status_code=404, detail="Digest not found")
    return JSONResponse(content=digest)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
