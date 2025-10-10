#!/usr/bin/env python3
"""
Usage (0-based column index):
  ./bin/add_from_csv.py <source_csv_path> <url_column_index>

Examples:
  ./bin/add_from_csv.py bin/import.csv 2        # take URLs from 3rd column (0-based)
  ./bin/add_from_csv.py bin/import.csv 0        # take URLs from 1st column

What this does:
- Reads/creates bin/redirects.csv (columns: URL, File).
- Reads the given source CSV and pulls URLs from the given 0-based column index.
- Auto-detects delimiter among [',',';','\\t','|'] with a reliable fallback (prefers ';' if present).
- Trims whitespace, skips empty values.
- Skips URLs already present in bin/redirects.csv (case-sensitive).
- Appends new rows as (URL=<url>, File="") and saves atomically.

Notes:
- If your source has a header row, just pick the correct 0-based column index; this script treats all rows uniformly.
"""

import sys
import os
import csv
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Set, List

import pandas as pd

CSV_PATH = Path("data/redirects.csv")


def atomic_overwrite_csv(df: pd.DataFrame, path: Path) -> None:
    """Atomically overwrite CSV at `path` with DataFrame `df` (UTF-8, no index)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=str(path.parent), newline="") as tmp:
        tmp_path = Path(tmp.name)
        df.to_csv(tmp_path, index=False, encoding="utf-8", quoting=csv.QUOTE_MINIMAL)
    os.replace(tmp_path, path)


def load_or_init_redirects(csv_path: Path) -> pd.DataFrame:
    """Load existing redirects CSV or initialize a new one with required columns."""
    if csv_path.exists():
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
        # Ensure required columns exist without dropping others.
        if "URL" not in df.columns:
            df["URL"] = ""
        if "File" not in df.columns:
            df["File"] = ""
        # Normalize
        df["URL"] = df["URL"].astype(str).str.strip()
        df["File"] = df["File"].astype(str).str.strip()
        return df
    else:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        return pd.DataFrame({"URL": pd.Series(dtype="string"), "File": pd.Series(dtype="string")})


def detect_delimiter(path: Path) -> str:
    """Detect delimiter among common options; prefer ';' if present in sample."""
    candidates = [",", ";", "\t", "|"]
    try:
        sample = path.read_text(encoding="utf-8-sig", errors="ignore")[:10000]
    except Exception:
        # Fallback: default to comma
        return ","
    # Quick preference for ';' if clearly present
    if ";" in sample and "," not in sample:
        return ";"
    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(sample, delimiters="".join(candidates))
        if getattr(dialect, "delimiter", None) in candidates:
            return dialect.delimiter
    except Exception:
        pass
    # Heuristic fallback: choose the candidate that appears most
    counts = {d: sample.count(d) for d in candidates}
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else ","


def extract_urls_with_csv_reader(source_csv: Path, col_0_based: int) -> List[str]:
    """Extract trimmed URLs from the given 0-based column using csv.reader (robust to ragged rows)."""
    if col_0_based < 0:
        print(f"Invalid column index {col_0_based}. Must be >= 0.", file=sys.stderr)
        sys.exit(2)

    delimiter = detect_delimiter(source_csv)
    urls: List[str] = []
    try:
        with source_csv.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=delimiter)
            for row_num, row in enumerate(reader, start=1):
                # Skip completely empty rows
                if not row or all((c or "").strip() == "" for c in row):
                    continue
                if col_0_based >= len(row):
                    # Row doesn't have that many columns; skip gracefully
                    continue
                val = (row[col_0_based] or "").strip()
                if val:
                    urls.append(val)
    except FileNotFoundError:
        print(f"Source CSV not found: {source_csv}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading source CSV '{source_csv}': {e}", file=sys.stderr)
        sys.exit(2)

    return urls


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 1

    source_csv = Path(sys.argv[1])
    try:
        col_idx = int(sys.argv[2])
    except ValueError:
        print("The column index must be an integer (0-based).", file=sys.stderr)
        return 1

    if not source_csv.exists():
        print(f"Source CSV not found: {source_csv}", file=sys.stderr)
        return 1

    # Load destination CSV (or init)
    redirects_df = load_or_init_redirects(CSV_PATH)

    # Existing URLs set for quick duplicate checks (case-sensitive)
    existing_urls: Set[str] = set(redirects_df["URL"].tolist())

    # Extract URLs from the specified 0-based column (robust parsing)
    urls = extract_urls_with_csv_reader(source_csv, col_idx)

    to_append = []
    skipped_empty = 0
    skipped_dupes = 0
    added = 0

    for url in urls:
        if not url:
            skipped_empty += 1
            continue
        if url in existing_urls:
            skipped_dupes += 1
            continue
        to_append.append({"URL": url, "File": ""})
        existing_urls.add(url)  # prevent duplicates within this import

    if to_append:
        add_df = pd.DataFrame(to_append, columns=["URL", "File"])
        # Keep any extra columns from the original CSV by aligning columns.
        all_cols = list(redirects_df.columns)
        for col in ["URL", "File"]:
            if col not in all_cols:
                all_cols.append(col)

        redirects_df = pd.concat([redirects_df, add_df], ignore_index=True)
        redirects_df = redirects_df.reindex(columns=all_cols)

        try:
            atomic_overwrite_csv(redirects_df, CSV_PATH)
            added = len(to_append)
            print(f"Appended {added} new URL(s) to {CSV_PATH}")
        except Exception as e:
            print(f"Failed to write CSV: {e}", file=sys.stderr)
            return 1
    else:
        print("No new URLs to append.")

    print(
        f"Summary:\n"
        f"  Added: {added}\n"
        f"  Skipped (empty): {skipped_empty}\n"
        f"  Skipped (duplicates): {skipped_dupes}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
