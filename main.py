import os
import json
from dotenv import load_dotenv
from src.collectors.youtube import YouTubeCollector
from src.collectors.forum import ForumCollector
from src.collectors.google_trends import GoogleTrendsCollector # <--- NEW IMPORT

load_dotenv()

def main():
    # 1. Setup Collectors
    yt_collector = YouTubeCollector()
    forum_collector = ForumCollector()
    trends_collector = GoogleTrendsCollector() # <--- NEW INIT

    all_data = []

    # 2. Collect YouTube
    print("--- Starting YouTube Collection ---")
    all_data.extend(yt_collector.fetch_workflows(country_code="US"))
    all_data.extend(yt_collector.fetch_workflows(country_code="IN"))

    # 3. Collect Forum
    print("\n--- Starting Forum Collection ---")
    all_data.extend(forum_collector.fetch_workflows(period="monthly"))

    # 4. Collect Google Trends
    print("\n--- Starting Google Trends Collection ---")
    all_data.extend(trends_collector.fetch_trends(country_code="US"))
    all_data.extend(trends_collector.fetch_trends(country_code="IN"))

    # 5. Save
    output_path = "data/workflows.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ Total Workflows Collected: {len(all_data)}")
    print(f"📁 Saved to {output_path}")

if __name__ == "__main__":
    main()