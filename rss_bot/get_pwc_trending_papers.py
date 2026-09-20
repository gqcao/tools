#!/usr/bin/env python3
"""Convert the Papers with Code trending-papers JSON response to RSS 2.0."""

import argparse
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.dom import minidom


def parse_pub_date(value):
    """Return an RFC 822 date, or None when the API has no valid date."""
    if not value:
        return None
    try:
        date = datetime.fromisoformat(value)
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        return format_datetime(date.astimezone(timezone.utc), usegmt=True)
    except (TypeError, ValueError):
        return None


def paper_link(paper):
    arxiv_id = paper.get("arxiv_id")
    if arxiv_id:
        return f"https://arxiv.org/abs/{arxiv_id}"
    source_url = paper.get("source_url")
    if source_url:
        return source_url
    return f"https://paperswithcode.com/paper/{paper.get('paper_id', '')}"


def item_description(paper):
    description = paper.get("abstract") or ""
    authors = paper.get("authors") or []
    if authors:
        description += f"\n\nAuthors: {', '.join(authors)}"

    tasks = [task.get("name") for task in paper.get("tasks") or [] if task.get("name")]
    if tasks:
        description += f"\n\nTasks: {', '.join(tasks)}"

    repository = paper.get("repository") or {}
    repository_url = repository.get("url")
    if repository_url:
        description += f"\n\nCode: {repository_url}"
    return description or paper.get("title") or "Papers with Code paper"


API_URL = "https://paperswithcode.co/api/v1/papers/trending?limit=20&max_age_days=7"


def fetch_papers(url):
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "rss-bot"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise ValueError("expected the API response to be a JSON array")
    return payload


def convert(papers):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Papers with Code Trending Papers"
    ET.SubElement(channel, "link").text = "https://paperswithcode.com/"
    ET.SubElement(channel, "description").text = "Trending papers from Papers with Code"
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(
        datetime.now(timezone.utc), usegmt=True
    )

    for paper in papers:
        title = paper.get("title") or "Untitled paper"
        link = paper_link(paper)
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "link").text = link
        ET.SubElement(item, "guid", isPermaLink="true").text = link
        ET.SubElement(item, "description").text = item_description(paper)
        pub_date = parse_pub_date(paper.get("date_published"))
        if pub_date:
            ET.SubElement(item, "pubDate").text = pub_date

    return minidom.parseString(ET.tostring(rss, encoding="unicode")).toprettyxml(indent="  ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", required=True, help="RSS XML output file")
    parser.add_argument("--url", default=API_URL, help="Papers with Code API URL")
    args = parser.parse_args()

    try:
        papers = fetch_papers(args.url)
        with open(args.output, "w", encoding="utf-8") as destination:
            destination.write(convert(papers))
    except (OSError, json.JSONDecodeError, urllib.error.URLError, ValueError) as error:
        print(f"Error fetching or converting Papers with Code JSON: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
