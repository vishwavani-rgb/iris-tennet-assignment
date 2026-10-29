
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import xml.etree.ElementTree as ET

import requests

from config import REQUEST_TIMEOUT_SECONDS, SOURCE_URL, USER_AGENT


JAO_RSS_URL = "https://www.jao.eu/news/messageboard/jao/feed/rss.rss"


def fetch_congestion_areas(
    url: str = SOURCE_URL,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
) -> dict[str, Any]:
   
    params = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "false",
        "f": "json",
    }
    response = requests.get(
        url,
        params=params,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()

    if payload.get("error"):
        raise RuntimeError(f"ArcGIS API error: {payload['error']}")

    return {
        "source_url": response.url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "fields": [field["name"] for field in payload.get("fields", [])],
        "records": [
            feature.get("attributes", {})
            for feature in payload.get("features", [])
        ],
    }


def fetch_jao_notices(
    url: str = JAO_RSS_URL,
    timeout: int = REQUEST_TIMEOUT_SECONDS,
) -> dict[str, Any]:
   
    response = requests.get(
        url,
        headers={
            "Accept": "application/rss+xml, application/xml, text/xml",
            "User-Agent": USER_AGENT,
        },
        timeout=timeout,
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)
    items = root.findall("./channel/item")
    records = []

    for item in items:
        title = item.findtext("title", default="").strip()
        link = item.findtext("link", default="").strip()
        published_at = item.findtext("pubDate", default="").strip()
        description = item.findtext("description", default="").strip()

        searchable = f"{title}\n{description}"
        if "tennet" not in searchable.lower():
            continue

        records.append({
            "notice_title": title,
            "notice_url": link,
            "published_at": published_at,
            "description": description,
        })

    return {
        "source_url": response.url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "records": records,
    }
