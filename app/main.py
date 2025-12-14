import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from collections import defaultdict

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from app.services.threat_feed import ThreatFeedService
from app.services.security_calculator import SecurityCalculator, AssessmentResponse
from app.services.tools_directory import ToolsDirectoryService

# Load environment variables
load_dotenv()

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
async def home(request: Request):
    """Home page rendering the latest digest and dashboard stats."""
    index = load_index()
    latest_digest = None
    past_digests = []

    if index:
        latest_date = index[0]
        latest_digest = load_digest(latest_date)
        
        # Load past digests (limit to 5)
        for date in index[1:6]:
            digest = load_digest(date)
            if digest:
                past_digests.append(digest)
    
    # Fetch stats for dashboard
    threat_service = ThreatFeedService()
    cves = await threat_service.fetch_recent_cves(days=30, limit=50)
    total_recent_cves = len(cves)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "latest_digest": latest_digest,
            "past_digests": past_digests,
            "has_digests": bool(latest_digest),
            "total_recent_cves": total_recent_cves
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


# Threat Feed Routes
@app.get("/threat-feed", response_class=HTMLResponse)
async def threat_feed_page(request: Request):
    """Threat feed dashboard with live CVE data."""
    threat_service = ThreatFeedService()
    
    # Fetch recent CVEs (match the stats window for consistency)
    cves = await threat_service.fetch_recent_cves(days=30, limit=50)
    
    # Get severity distribution (calculated from the same service logic, but we want to ensure consistency)
    # Ideally, we should use the SAME dataset for both.
    # Let's calculate stats from the fetched CVEs directly to ensure 100% match between table and charts on this page view.
    
    severity_counts = defaultdict(int)
    category_counts = defaultdict(int)
    
    categories = {
        "Web Application": ["xss", "sql injection", "csrf", "web", "http"],
        "Network": ["network", "protocol", "tcp", "udp", "dns"],
        "Authentication": ["authentication", "password", "credential", "login"],
        "Privilege Escalation": ["privilege", "escalation", "root", "admin"],
        "Code Execution": ["remote code execution", "rce", "execute", "arbitrary code"],
        "Data Exposure": ["information disclosure", "data leak", "exposure", "sensitive"]
    }
    
    for cve in cves:
        severity_counts[cve["severity"]] += 1
        
        desc = cve["description"].lower()
        found_category = False
        for category, keywords in categories.items():
            if any(keyword in desc for keyword in keywords):
                category_counts[category] += 1
                found_category = True
                break
        if not found_category:
            category_counts["Other"] += 1
            
    # Format distribution for charts based on THIS dataset
    severity_dist = {
        "labels": ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
        "data": [
            severity_counts.get("CRITICAL", 0),
            severity_counts.get("HIGH", 0),
            severity_counts.get("MEDIUM", 0),
            severity_counts.get("LOW", 0)
        ],
        "percentages": [0, 0, 0, 0], # Calculated in JS or ignored if simple count
        "total": len(cves)
    }
    
    category_dist = {
        "labels": list(categories.keys()),
        "data": [category_counts.get(cat, 0) for cat in categories.keys()]
    }
    
    return templates.TemplateResponse(
        "threat_feed.html",
        {
            "request": request,
            "cves": cves,
            "total_cves": len(cves),
            "critical_count": severity_counts.get("CRITICAL", 0),
            "high_count": severity_counts.get("HIGH", 0),
            "medium_count": severity_counts.get("MEDIUM", 0),
            "severity_distribution": severity_dist,
            "category_distribution": category_dist
        }
    )


@app.get("/api/threats/recent")
async def api_recent_threats(days: int = 7, limit: int = 50):
    """API endpoint for recent threats."""
    threat_service = ThreatFeedService()
    cves = await threat_service.fetch_recent_cves(days=days, limit=limit)
    return JSONResponse(content={"cves": cves, "count": len(cves)})


@app.get("/api/threats/severity-distribution")
async def api_severity_distribution(days: int = 30):
    """API endpoint for severity distribution data."""
    threat_service = ThreatFeedService()
    distribution = await threat_service.get_severity_distribution(days=days)
    return JSONResponse(content=distribution)


@app.get("/api/threats/category-distribution")
async def api_category_distribution(days: int = 30):
    """API endpoint for category distribution data."""
    threat_service = ThreatFeedService()
    distribution = await threat_service.get_category_distribution(days=days)
    return JSONResponse(content=distribution)


# Security Calculator Routes
@app.get("/security-calculator", response_class=HTMLResponse)
async def security_calculator_page(request: Request):
    """Security assessment calculator page."""
    calculator = SecurityCalculator()
    questions = calculator.get_all_questions()
    
    return templates.TemplateResponse(
        "security_calculator.html",
        {
            "request": request,
            "questions": questions
        }
    )


@app.post("/api/calculate-score")
async def calculate_security_score(response: AssessmentResponse):
    """Calculate security score based on assessment responses."""
    calculator = SecurityCalculator()
    result = calculator.calculate_score(response)
    return JSONResponse(content=result)


# Tools Directory Routes
@app.get("/tools", response_class=HTMLResponse)
async def tools_directory_page(request: Request):
    """Security tools directory page."""
    tools_service = ToolsDirectoryService()
    tools = tools_service.get_all_tools()
    categories = tools_service.get_categories()
    
    return templates.TemplateResponse(
        "tools_directory.html",
        {
            "request": request,
            "tools": tools,
            "categories": categories
        }
    )
