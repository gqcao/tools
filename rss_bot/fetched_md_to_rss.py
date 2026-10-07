import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
import sys
import argparse
import time
import urllib.error
import urllib.request

def fetch_markdown_from_url(
    url: str,
    max_retries: int = 5,
    retry_delay: int = 3,
    response_wait: int = 10,
) -> str:
    """
    Fetches markdown content from the specified URL with retry logic.
    Retries if the response contains CAPTCHA/blocked page indicators.
    """
    # r.jina.ai is fronted by Cloudflare.  Its challenge page can be
    # triggered by old, highly specific browser UAs (such as Chrome 91).
    # This generic UA is accepted by the endpoint and does not pretend to be
    # a browser version that may have an inconsistent fingerprint.
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/plain, */*',
    }

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Fetching content from {url} (attempt {attempt}/{max_retries})...")
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=60) as response:
                # r.jina.ai may report verification success before the
                # upstream conversion response is ready.
                if response_wait > 0:
                    print(f"Waiting {response_wait} seconds for the response...")
                    time.sleep(response_wait)
                text = response.read().decode(response.headers.get_content_charset() or 'utf-8')

            # Check if the response is a verification/interstitial page. Jina
            # may return this temporarily while its upstream browser session
            # is being established, so let the retry loop wait for it.
            blocked_markers = (
                "Just a moment...",
                "Please confirm",
                "CAPTCHA",
                "cf-mitigated",
                "Verification successful",
                "Waiting for r.jina.ai to respond",
            )
            if not text.strip() or any(marker in text for marker in blocked_markers):
                raise RuntimeError("received an empty or verification page")

            return text

        except (urllib.error.URLError, urllib.error.HTTPError, RuntimeError) as e:
            print(f"Error fetching URL (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise RuntimeError("All retries exhausted while fetching the URL") from e

def extract_embedded_rss(md_content: str) -> str | None:
    """Extract and validate RSS XML embedded in a Jina Markdown response."""
    start = md_content.find("<?xml")
    if start < 0:
        start = md_content.find("<rss")
    end = md_content.rfind("</rss>")
    if start < 0 or end < 0:
        return None

    xml = md_content[start:end + len("</rss>")].strip()
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return None
    if root.tag.rsplit("}", 1)[-1].lower() != "rss":
        return None
    return xml + "\n"


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
    parser = argparse.ArgumentParser(description="Fetch markdown from an RSS feed via Jina AI and convert to RSS XML.")
    parser.add_argument("-s", type=str, required=True, help="The RSS URL to fetch markdown content from (e.g., https://cacm.acm.org/section/news/feed)")
    parser.add_argument("-o", type=str, required=True, help="The output XML file path (e.g., channels/cacm_magazine.xml)")
    parser.add_argument("--retries", type=int, default=10, help="Maximum number of retry attempts (default: 10)")
    parser.add_argument("--delay", type=int, default=10, help="Delay in seconds between retries (default: 10)")
    parser.add_argument("--response-wait", type=int, default=10, help="Seconds to wait after the HTTP response arrives before reading its body (default: 10)")
    args = parser.parse_args()

    # Accept both the source URL (https://cacm.acm.org/feed) and an already
    # wrapped Jina URL (https://r.jina.ai/https://cacm.acm.org/feed).
    url = args.s if args.s.startswith("https://r.jina.ai/") else f"https://r.jina.ai/{args.s}"

    markdown_content = fetch_markdown_from_url(
        url,
        max_retries=args.retries,
        retry_delay=args.delay,
        response_wait=args.response_wait,
    )

    if not markdown_content:
        print("No content fetched.")
        sys.exit(1)

    print("Parsing content and generating RSS feed...")
    # Jina normally returns Markdown, but for an RSS source it may embed the
    # original XML after its metadata. Preserve that feed instead of treating
    # the XML as article-less Markdown.
    rss_output = extract_embedded_rss(markdown_content)
    if rss_output is None:
        rss_output = parse_markdown_to_rss(markdown_content)

    try:
        with open(args.o, 'w', encoding='utf-8') as f:
            f.write(rss_output)
        print(f"\nRSS feed saved to {args.o}")
    except Exception as e:
        print(f"Error saving file: {e}")
