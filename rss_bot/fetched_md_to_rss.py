import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import sys
import requests

def fetch_markdown_from_url(url: str) -> str:
    """
    Fetches markdown content from the specified URL.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)

def parse_markdown_to_rss(md_content: str, channel_title: str = "Communications of the ACM", channel_link: str = "https://cacm.acm.org/", channel_description: str = "Latest articles from Communications of the ACM") -> str:
    """
    Parses specific markdown format from CACM feed and converts to RSS 2.0 XML.
    """
    
    # We split by '### ' to get individual items, then process each
    parts = md_content.split('### ')
    
    items = []
    
    for part in parts:
        if not part.strip():
            continue
            
        # Extract Title and Link from the first line: [Title](Link)
        title_match = re.match(r'\[([^\]]+)\]\(([^)]+)\)', part)
        if not title_match:
            continue
            
        title = title_match.group(1)
        link = title_match.group(2)
        
        # Extract Date
        # Looking for a pattern like: Mon, 30 Mar 2026 19:54:55 +0000
        date_match = re.search(r'([A-Z][a-z]{2}, \d{2} [A-Z][a-z]{2} \d{4} \d{2}:\d{2}:\d{2} [+\-]\d{4})', part)
        pub_date_str = ""
        if date_match:
            pub_date_str = date_match.group(1)
            
        # Clean up description: Take the rest of the text after the link/title block
        # For this specific feed, the "content" is often just the link repeated or empty.
        # We'll use the title as the description if no other text is found, or strip the metadata lines.
        description = title
        
        items.append({
            'title': title,
            'link': link,
            'pubDate': pub_date_str,
            'description': description
        })

    # Build RSS XML
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    # Channel Metadata
    ET.SubElement(channel, "title").text = channel_title
    ET.SubElement(channel, "link").text = channel_link
    ET.SubElement(channel, "description").text = channel_description
    
    # Current build time
    now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    ET.SubElement(channel, "lastBuildDate").text = now

    # Add Items
    for item_data in items:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = item_data['title']
        ET.SubElement(item, "link").text = item_data['link']
        ET.SubElement(item, "description").text = item_data['description']
        if item_data['pubDate']:
            ET.SubElement(item, "pubDate").text = item_data['pubDate']

    # Pretty Print XML
    rough_string = ET.tostring(rss, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

if __name__ == "__main__":
    # URL to fetch markdown content from
    url = "https://r.jina.ai/https://cacm.acm.org/issue/latest/feed"
    
    print(f"Fetching content from {url}...")
    markdown_content = fetch_markdown_from_url(url)
    
    if not markdown_content:
        print("No content fetched.")
        sys.exit(1)
        
    print("Parsing content and generating RSS feed...")
    rss_output = parse_markdown_to_rss(markdown_content)
    
    # Print to console
    # print(rss_output)
    
    # Optional: Save to an XML file
    output_filename = "./channels/cacm_feed.xml"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(rss_output)
        print(f"\nRSS feed saved to {output_filename}")
    except Exception as e:
        print(f"Error saving file: {e}")
