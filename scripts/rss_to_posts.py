import feedparser
import os
from datetime import datetime
import yaml

# RSS feed URL from environment variable
RSS_FEED_URL = os.getenv("RSS_FEED_URL")
POSTS_DIR = "_posts"

# Ensure _posts directory exists
if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

# Fetch RSS feed
feed = feedparser.parse(RSS_FEED_URL)

# Process each entry
for entry in feed.entries[:5]:  # Limit to 5 latest posts
    title = entry.title.replace(":", " -")  # Clean title for filename
    date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
    filename = f"{date.strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')[:50]}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    # Skip if post already exists
    if os.path.exists(filepath):
        continue

    # Recreate content (summary + link to original)
    content = f"{entry.description[:200]}... [Read more]({entry.link})"

    # Front matter for Jekyll
    front_matter = {
        "layout": "post",
        "title": title,
        "date": date.strftime("%Y-%m-%d %H:%M:%S %z"),
        "original_link": entry.link
    }

    # Write the blog post
    with open(filepath, "w") as f:
        f.write("---\n")
        f.write(yaml.dump(front_matter))
        f.write("---\n\n")
        f.write(content)

print("Posts generated successfully!")
