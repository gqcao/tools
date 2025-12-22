#!/bin/sh

# Navigate to repository root
cd "$(dirname "$0")"

# Create channels directory if it doesn't exist
mkdir -p channels

# Download RSS feeds
curl -s https://mags.acm.org/communications/rss -o channels/cacm_feed.xml
curl -s https://techcrunch.com/feed/ -o channels/techcrunch.xml
curl -s https://techcrunch.com/category/startups/feed/ -o channels/techcrunch_startups.xml

# Git operations
git add .
git commit -m "Update RSS feeds - $(date)"
git push --quiet https://${GITHUB_TOKEN}@github.com/gqcao/rss_bot.git main >/dev/null 2>&1
