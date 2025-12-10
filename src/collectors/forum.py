import requests
from typing import List, Dict, Any

class ForumCollector:
    def __init__(self):
        self.base_url = "https://community.n8n.io"

    def fetch_workflows(self, period: str = "monthly", limit: int = 50) -> List[Dict[str, Any]]:
        """
        Fetches top topics from the n8n Discourse forum.
        """
        print(f"💬 Fetching Forum data (Period: {period})...")
        
        workflows = []
        # Discourse pagination often uses 'page' query param, but 'top.json' returns a list in 'topic_list'.
        # We'll fetch the top list.
        try:
            url = f"{self.base_url}/top.json?period={period}"
            response = requests.get(url)
            
            if response.status_code != 200:
                print(f"❌ Error fetching forum data: Status {response.status_code}")
                return []
            
            data = response.json()
            topics = data.get("topic_list", {}).get("topics", [])

            for topic in topics[:limit]:
                # Extract metrics
                title = topic.get("title")
                slug = topic.get("slug")
                topic_id = topic.get("id")
                
                views = topic.get("views", 0)
                likes = topic.get("like_count", 0)
                posts_count = topic.get("posts_count", 0)
                # 'posters' is a list of objects, length = unique contributors roughly
                contributors = len(topic.get("posters", []))

                # Construct the entry
                entry = {
                    "workflow": title,
                    "platform": "n8n Forum",
                    "url": f"{self.base_url}/t/{slug}/{topic_id}",
                    "popularity_metrics": {
                        "views": views,
                        "likes": likes,
                        "replies": posts_count - 1, # Subtract 1 because usually OP is counted
                        "contributors": contributors
                    },
                    # Forums don't have the same ratio logic as YT, but we can approximate or leave None
                    "like_to_view_ratio": round(likes / views, 4) if views > 0 else 0.0,
                    "comment_to_view_ratio": round((posts_count - 1) / views, 4) if views > 0 else 0.0,
                    "country": "Global" 
                }
                workflows.append(entry)

        except Exception as e:
            print(f"❌ Exception occurred in ForumCollector: {e}")

        return workflows