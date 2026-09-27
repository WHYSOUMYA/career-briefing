"""
Pulls fresh headlines for the career briefing dashboard and writes data.json.
Run manually with: python scraper.py
Runs automatically once a day via .github/workflows/update.yml
"""

import json
from datetime import datetime, timezone
from urllib.parse import quote

import feedparser

# Each category is a Google News search query. Edit these to change what
# the dashboard tracks.
CATEGORIES = {
    "affairs": "AI agentic hiring OR AI industry India",
    "layoffs": "tech layoffs India OR tech layoffs 2026",
    "placements": "campus placements India 2026 OR GCC hiring India",
    "india": "India news today",
    "sports": "tennis news OR Formula 1 news",
}

MAX_ITEMS_PER_CATEGORY = 6


def fetch_category(query):
    url = (
        "https://news.google.com/rss/search?q="
        f"{quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    )
    feed = feedparser.parse(url)

    items = []
    for entry in feed.entries[:MAX_ITEMS_PER_CATEGORY]:
        source = ""
        if hasattr(entry, "source") and hasattr(entry.source, "title"):
            source = entry.source.title
        items.append(
            {
                "title": entry.get("title", "").split(" - ")[0].strip(),
                "link": entry.get("link", ""),
                "source": source,
                "published": entry.get("published", ""),
            }
        )
    return items


def main():
    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "categories": {},
    }
    for key, query in CATEGORIES.items():
        print(f"Fetching '{key}'...")
        data["categories"][key] = fetch_category(query)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Wrote data.json")


if __name__ == "__main__":
    main()
