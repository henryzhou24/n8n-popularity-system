from pytrends.request import TrendReq
import time
from typing import List, Dict, Any

class GoogleTrendsCollector:
    def __init__(self):
        # Initialize pytrends
        # retries and backoff_factor help with stability
        self.pytrends = TrendReq(hl='en-US', tz=360, retries=2, backoff_factor=0.1)
        self.keywords = [
            "n8n automation", "n8n tutorial", "n8n workflow", 
            "n8n gmail", "n8n slack"
        ]

    def fetch_trends(self, country_code: str = "US") -> List[Dict[str, Any]]:
        print(f"📈 Fetching Google Trends data for {country_code}...")
        results = []
        
        try:
            # We take the first 5 keywords (API limit per request is 5)
            batch = self.keywords[:5]
            
            # Build payload
            self.pytrends.build_payload(batch, cat=0, timeframe='today 3-m', geo=country_code, gprop='')
            
            # Get Interest Over Time
            data = self.pytrends.interest_over_time()
            
            if data.empty:
                print("⚠️ No trends data returned.")
                return []

            for keyword in batch:
                if keyword not in data.columns:
                    continue
                    
                series = data[keyword]
                if len(series) == 0: continue

                # Get latest interest score (0-100)
                current_interest = int(series.iloc[-1])
                
                # Check trend (Last value vs First value)
                start_interest = int(series.iloc[0])
                trend_msg = "Stable"
                if current_interest > start_interest * 1.2:
                    trend_msg = "Trending Up 📈"
                elif current_interest < start_interest * 0.8:
                    trend_msg = "Trending Down 📉"
                
                entry = {
                    "workflow": f"Keyword: {keyword}",
                    "platform": "Google Search",
                    "url": f"https://trends.google.com/trends/explore?q={keyword.replace(' ', '%20')}",
                    "popularity_metrics": {
                        "relative_interest_score": current_interest,
                        "trend_status": trend_msg
                    },
                    "like_to_view_ratio": 0.0,
                    "comment_to_view_ratio": 0.0,
                    "country": country_code
                }
                results.append(entry)
            
            # Be nice to the API
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Google Trends Error: {e}")
            print("   (This is common with free scrapers. In production, use Google Ads API.)")

        return results