import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Any

class YouTubeCollector:
    def __init__(self):
        # Load API key from environment variable for security
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not found in environment variables")
        
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def fetch_workflows(self, query: str = "n8n workflow", country_code: str = "US", max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Fetches videos matching the query from a specific country,
        retrieves statistics, and calculates engagement ratios.
        """
        print(f"🎥 Fetching YouTube data for '{query}' in {country_code}...")
        
        workflows = []

        try:
            # 1. Search for videos
            search_response = self.youtube.search().list(
                q=query,
                type="video",
                part="id,snippet",
                regionCode=country_code,
                maxResults=max_results,
                relevanceLanguage="en" 
            ).execute()

            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

            if not video_ids:
                print("No videos found.")
                return []

            # 2. Get detailed statistics for these videos
            stats_response = self.youtube.videos().list(
                part="statistics,snippet",
                id=','.join(video_ids)
            ).execute()

            # 3. Process and format the data
            for item in stats_response.get('items', []):
                stats = item['statistics']
                snippet = item['snippet']

                # specific metrics extraction (default to 0 if hidden/missing)
                views = int(stats.get('viewCount', 0))
                likes = int(stats.get('likeCount', 0))
                comments = int(stats.get('commentCount', 0))

                # Safe division for ratios
                like_ratio = round(likes / views, 4) if views > 0 else 0.0
                comment_ratio = round(comments / views, 4) if views > 0 else 0.0

                entry = {
                    "workflow": snippet['title'],
                    "platform": "YouTube",
                    "url": f"https://www.youtube.com/watch?v={item['id']}",
                    "popularity_metrics": {
                        "views": views,
                        "likes": likes,
                        "comments": comments
                    },
                    "like_to_view_ratio": like_ratio,
                    "comment_to_view_ratio": comment_ratio,
                    "country": country_code
                }
                workflows.append(entry)

        except HttpError as e:
            print(f"❌ An HTTP error occurred: {e}")
        
        return workflows