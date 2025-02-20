import feedparser
import os
from datetime import datetime
import yaml

RSS_FEED_URL = os.getenv("RSS_FEED_URL", "https://timesofindia.indiatimes.com/rssfeeds/4719161.cms")
POSTS_DIR = "_posts"

if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

feed = feedparser.parse(RSS_FEED_URL)
print(f"Feed entries found: {len(feed.entries)}")

if not feed.entries:
    print("No entries in RSS feed. Exiting.")
    exit(0)

for entry in feed.entries[:5]:
    try:
        title = entry.get("title", "Untitled").replace(":", " -")
        date = datetime.strptime(entry.get("published", datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")), 
                               "%a, %d %b %Y %H:%M:%S %z")
        filename = f"{date.strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')[:50]}.md"
        filepath = os.path.join(POSTS_DIR, filename)

        if os.path.exists(filepath):
            print(f"Skipping existing post: {filename}")
            continue

        content = f"{entry.get('description', 'No description available')[:200]}... [Read more]({entry.link})"
        front_matter = {
            "layout": "post",
            "title": title,
            "date": date.strftime("%Y-%m-%d %H:%M:%S %z"),
            "original_link": entry.link
        }

        with open(filepath, "w") as f:
            f.write("---\n")
            f.write(yaml.dump(front_matter))
            f.write("---\n\n")
            f.write(content)
        print(f"Created post: {filename}")
    except Exception as e:
        print(f"Error processing entry '{title}': {e}")
