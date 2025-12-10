from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import json
import os

# Initialize the API
app = FastAPI(
    title="n8n Popularity System API",
    description="API to retrieve popular n8n workflows from YouTube, Forums, and Google.",
    version="1.0.0"
)

DATA_PATH = "data/workflows.json"

def load_data():
    """Helper to load the latest JSON data."""
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def home():
    """Health check endpoint."""
    return {"status": "active", "message": "Go to /docs to see the API documentation."}

@app.get("/workflows")
def get_workflows(
    platform: Optional[str] = Query(None, description="Filter by platform (e.g., 'YouTube', 'n8n Forum')"),
    country: Optional[str] = Query(None, description="Filter by country (e.g., 'US', 'IN')"),
    min_views: Optional[int] = Query(0, description="Minimum number of views")
):
    """
    Retrieve n8n workflows with optional filtering.
    """
    data = load_data()
    
    if not data:
        raise HTTPException(status_code=404, detail="No data found. Please run the collector script first.")

    # 1. Filter by Platform
    if platform:
        # Case-insensitive matching
        data = [w for w in data if w.get("platform", "").lower() == platform.lower()]

    # 2. Filter by Country
    if country:
        data = [w for w in data if w.get("country", "").lower() == country.lower()]
        
    # 3. Filter by Views (demonstrates "Business Logic")
    if min_views > 0:
        data = [w for w in data if w["popularity_metrics"].get("views", 0) >= min_views]

    return {
        "count": len(data),
        "data": data
    }