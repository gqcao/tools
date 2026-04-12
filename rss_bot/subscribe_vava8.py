import re
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone, timedelta

def parse_chinese_relative_time(text_block: str, base_time: datetime) -> datetime:
    """
    Searches a block of text for Chinese relative time patterns like '14小时前'.
    Returns the calculated datetime.
    """
    if not text_block:
        return base_time
    
    # Look for pattern: Number + "小时" or "时" + "前"
    # Example: "14小时前", "2小时前"
    match = re.search(r'(\d+)\s*(?:小时|时)\s*前', text_block)
    
    if match:
        hours = int(match.group(1))
        return base_time - timedelta(hours=hours)
        
    return base_time

def fetch_and_generate_rss():
    # 1. Fetch Markdown content
    url = "https://www.vava8.com/"
    jina_url = f"https://r.jina.ai/{url}"
    
    try:
        response = requests.get(jina_url)
        response.raise_for_status()
        markdown_content = response.text
    except Exception as e:
        print(f"Error fetching content: {e}")
        return

    # 2. Parse Items
    lines = markdown_content.split('\n')
    items = []
    
    # Regex for Header: ## [Title](Link)
    header_regex = re.compile(r'^## \[(.*?)\]\((.*?)\)$')
    
    now_utc = datetime.now(timezone.utc)
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        header_match = header_regex.match(line)
        
        if header_match:
            title = header_match.group(1)
            link = header_match.group(2)
            pub_date = now_utc # Default to now
            
            # Look ahead up to 5 lines to find the time information
            # Structure:
            # ## [Title](Link)
            # [Image]...
            # [Source](Link)14小时前  <-- We want this line
            
            time_found = False
            for j in range(i + 1, min(i + 6, len(lines))):
                next_line = lines[j].strip()
                
                # If we hit another header, stop looking
                if next_line.startswith('## '):
                    break
                
                if not next_line:
                    continue
                
                # Check if this line contains the time pattern "X小时前"
                if '小时前' in next_line or '时前' in next_line:
                    pub_date = parse_chinese_relative_time(next_line, now_utc)
                    time_found = True
                    break
            
            items.append({
                'title': title,
                'link': link,
                'pub_date': pub_date
            })
        i += 1

    if not items:
        print("No items found.")
        return

    # 3. Generate RSS XML
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    
    ET.SubElement(channel, "title").text = "Vava8 News Feed"
    ET.SubElement(channel, "link").text = "https://www.vava8.com/"
    ET.SubElement(channel, "description").text = "Latest news from Vava8"
    
    # Format lastBuildDate
    def format_rfc822(dt):
        return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

    ET.SubElement(channel, "lastBuildDate").text = format_rfc822(now_utc)

    for item_data in items:
        item = ET.SubElement(channel, "item")
        
        ET.SubElement(item, "title").text = item_data['title']
        ET.SubElement(item, "link").text = item_data['link']
        
        # Description equals Title as requested
        ET.SubElement(item, "description").text = item_data['title']
        
        # Real calculated Pub Date
        ET.SubElement(item, "pubDate").text = format_rfc822(item_data['pub_date'])

    # 4. Output
    rough_string = ET.tostring(rss, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    xml_str = reparsed.toprettyxml(indent="  ")
    
    # print(xml_str)
    
    with open("./channels/vava8_feed.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)
    print("Saved to vava8_simple_feed.xml")

if __name__ == "__main__":
    fetch_and_generate_rss()
