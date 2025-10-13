#!/usr/bin/env python3
from pathlib import Path
import csv
import logging
import sys
import time
from typing import List
import requests
import json

from settings import MATTERMOST

# --- Config ---
CSV_PATH = Path("data/redirects.csv")
REQUEST_TIMEOUT_SECONDS = 10
SLEEP_BETWEEN_REQUESTS_SECONDS = 1

LOG_PATH = Path("logs/main.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.FileHandler(LOG_PATH, encoding="utf-8", mode="a")],
)
logger = logging.getLogger("url-checker")


def load_urls(csv_path: Path) -> List[str]:
    """Load all URL values from a CSV with a 'URL' header (case-insensitive)."""
    if not csv_path.exists():
        logger.error(f"CSV not found: {csv_path.resolve()}")
        sys.exit(1)

    urls: List[str] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            logger.error("CSV has no header row.")
            sys.exit(1)

        # Find the 'URL' column case-insensitively
        header_map = {h.lower(): h for h in reader.fieldnames}
        if "url" not in header_map:
            logger.error(f"CSV must have a 'URL' column. Found: {reader.fieldnames}")
            sys.exit(1)

        url_key = header_map["url"]

        for row in reader:
            raw = (row.get(url_key) or "").strip()
            if raw:
                urls.append(raw)

    # De-duplicate while preserving order
    seen = set()
    unique_urls = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique_urls.append(u)
    return unique_urls


def check_urls(urls: List[str]) -> List[str]:
    """Return a list of URLs that failed (non-2xx/3xx or request error)."""
    failed: list[str] = []
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "url-checker/1.0 (+https://example.local)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
    )

    logger.info(f"Checking {len(urls)} URLs")

    for url in urls:
        try:
            resp = session.get(
                url, timeout=REQUEST_TIMEOUT_SECONDS, allow_redirects=True
            )
            if not resp.ok:
                logger.error(
                    f"URL check failed for {url}: {resp.status_code} {resp.reason}"
                )
                failed.append(url)
        except requests.RequestException as e:
            logger.error(f"URL check threw error for {url}: {e}")
            failed.append(url)

        time.sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)

    return failed


def send_mattermost_message(message: str) -> bool:

    try:
        base_url = MATTERMOST.get("base_url", "").rstrip("/")
        token = MATTERMOST.get("token")
        channel_id = MATTERMOST.get("channel_id")
        payload = {"channel_id": channel_id, "message": message}

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        url = f"{base_url}/api/v4/posts?set_online=false"
        resp = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=10,
        )
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        # Mirror your previous logging style but correct the message
        logger.error(f"Failed to send Mattermost message: {e}")
        logger.exception(e)
        return False


def main() -> int:
    try:
        logger.info("Loading URLs from CSV...")
        urls = load_urls(CSV_PATH)
        if not urls:
            logger.warning("No URLs found in CSV.")
            return 0

        logger.info(f"Checking {len(urls)} URLs...")
        failed = check_urls(urls)

        if failed:
            logger.error("Some URLs failed. Sending Mattermost message...")
            message = "The following URLs failed:\n" + "\n".join(failed)
            send_mattermost_message(message)
        else:
            logger.info("All URLs responded OK.")
        return 0
    except Exception as e:
        logger.error(f"An error occurred while checking URLs: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
