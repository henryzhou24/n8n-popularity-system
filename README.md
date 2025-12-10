# n8n Workflow Popularity System

## 📋 Overview
A production-ready data pipeline and REST API designed to identify, quantify, and serve the popularity of n8n workflows across multiple platforms.

The system aggregates data from **YouTube**, **n8n Community Forums (Discourse)**, and **Google Search Trends**, normalizing the data into a unified JSON structure with calculated engagement metrics.

## ✨ Key Features
* **Multi-Source ETL Pipeline:**
    * **YouTube:** Fetches video statistics and calculates engagement ratios (`like_to_view`, `comment_to_view`) per the assignment formula.
    * **Forums:** Retrieves top discussions from the n8n Discourse community.
    * **Google Trends:** Tracks keyword interest over time (Trending Up/Down).
* **REST API:** Built with **FastAPI**, providing a high-performance backend with automatic interactive documentation (Swagger UI).
* **Segmentation:** Data is filterable by Platform (YouTube, Forum, Google) and Country (US, India).
* **Robust Automation:** Includes a local scheduler for daily updates and is compatible with CI/CD workflows (GitHub Actions).
* **Production Ready:** Uses environment variables for security, error handling for resilience, and modular code structure.

## 🛠️ Project Structure
```text
n8n-popularity-system/
├── data/
│   └── workflows.json       # Generated dataset (Persistent storage)
├── src/
│   ├── collectors/
│   │   ├── youtube.py       # YouTube Data API v3 implementation
│   │   ├── forum.py         # Discourse API implementation
│   │   └── google_trends.py # Pytrends implementation
├── api.py                   # FastAPI Server application
├── main.py                  # ETL Entry point (Data Collector)
├── scheduler.py             # Automation script (Daily Cron)
├── requirements.txt         # Project dependencies
└── .env                     # API Keys (Not included in repo)