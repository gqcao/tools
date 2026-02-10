#!/bin/sh

# Navigate to repository root
cd "$(dirname "$0")"

# Create channels directory if it doesn't exist
mkdir -p channels

# Download RSS feeds
curl -s https://mags.acm.org/communications/rss -o channels/cacm_feed.xml
curl -s https://techcrunch.com/feed/ -o channels/techcrunch.xml
curl -s https://techcrunch.com/category/startups/feed/ -o channels/techcrunch_startups.xml
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" https://www.efinancialcareers.com/feed/syndication/rss.xml -o channels/eficareers.xml

# Git operations
git add .
git commit -m "Update RSS feeds - $(date)"
git push --quiet https://${GITHUB_TOKEN}@github.com/gqcao/rss_bot.git main >/dev/null 2>&1
