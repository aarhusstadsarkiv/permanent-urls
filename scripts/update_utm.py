import pandas as pd
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

INPUT_CSV = "data/redirects.csv"
OUTPUT_CSV = "data/redirects.updated.csv"  # change to INPUT_CSV to overwrite

URL_COL = "URL"  # change if your column name differs


def add_utm_defaults(url: str) -> str:
    if not isinstance(url, str) or not url.strip():
        return url  # leave non-strings/empty as-is

    parsed = urlparse(url)
    qs = parse_qs(parsed.query, keep_blank_values=True)

    # Treat missing or empty as "not set"
    if "utm_source" not in qs or not any(v for v in qs["utm_source"]):
        qs["utm_source"] = ["qr"]
    if "utm_campaign" not in qs or not any(v for v in qs["utm_campaign"]):
        qs["utm_campaign"] = ["default"]

    new_query = urlencode(qs, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def main():
    df = pd.read_csv(INPUT_CSV)
    if URL_COL not in df.columns:
        raise ValueError(f"Column '{URL_COL}' not found in {INPUT_CSV}")

    df[URL_COL] = df[URL_COL].apply(add_utm_defaults)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Updated CSV written to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
