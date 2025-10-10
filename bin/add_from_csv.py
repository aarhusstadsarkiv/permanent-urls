#!/usr/bin/env python3
"""
Usage:
  ./bin/add_from_csv.py <source_csv_path> <url_column_number>

Example:
  ./bin/add_from_csv.py bin/import.csv 2

Behavior:
- Reads/creates bin/redirects.csv (columns: URL, File).
- Reads the given source CSV and pulls URLs from the given 1-based column number.
- Trims whitespace, skips empty values.
- Skips URLs already present in bin/redirects.csv (case-sensitive match).
- Appends new rows as (URL=<url>, File="") and saves atomically.

Notes:
- Column numbering is 1-based to match the example (2 => second column).
"""

import sys
import os
import csv
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Set

import pandas as pd

CSV_PATH = Path("bin/redirects.csv")


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


def extract_urls_from_source(source_csv: Path, col_1_based: int) -> list[str]:
    """Extract trimmed URLs from the given 1-based column in `source_csv`."""
    try:
        src_df = pd.read_csv(source_csv, dtype=str, keep_default_na=False)
    except Exception as e:
        print(f"Error reading source CSV '{source_csv}': {e}", file=sys.stderr)
        sys.exit(2)

    if src_df.shape[1] < col_1_based or col_1_based <= 0:
        print(
            f"Invalid column number {col_1_based}. Source CSV has {src_df.shape[1]} column(s).",
            file=sys.stderr,
        )
        sys.exit(2)

    # Convert 1-based to 0-based index
    col_idx = col_1_based - 1
    series = src_df.iloc[:, col_idx].astype(str).str.strip()
    # Keep non-empty values only
    urls = [u for u in series.tolist() if u]
    return urls


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 1

    source_csv = Path(sys.argv[1])
    try:
        col_num = int(sys.argv[2])
    except ValueError:
        print("The column number must be an integer (1-based).", file=sys.stderr)
        return 1

    if not source_csv.exists():
        print(f"Source CSV not found: {source_csv}", file=sys.stderr)
        return 1

    # Load destination CSV (or init)
    redirects_df = load_or_init_redirects(CSV_PATH)

    # Existing URLs set for quick duplicate checks (case-sensitive)
    existing_urls: Set[str] = set(redirects_df["URL"].tolist())

    # Extract URLs from the specified column in the source CSV
    urls = extract_urls_from_source(source_csv, col_num)

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
        existing_urls.add(url)  # prevent duplicates within the source itself

    if to_append:
        add_df = pd.DataFrame(to_append, columns=["URL", "File"])
        # Keep any extra columns from the original CSV by aligning columns.
        # New rows only have URL and File; other columns (if any) will be NaN -> write as empty.
        all_cols = list(redirects_df.columns)
        for col in ["URL", "File"]:
            if col not in all_cols:
                all_cols.append(col)

        redirects_df = pd.concat([redirects_df, add_df], ignore_index=True)
        # Reorder to original columns if possible
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
