#!/usr/bin/env python3
"""
Generate simple HTML redirect files from bin/redirects.csv using pandas.

Behavior:
- Rows without a URL are skipped (warned).
- If 'File' is provided:
    - Ensure it ends with .html.
    - If that file already exists on disk, skip (do not overwrite).
    - If it does not exist, create it.
- If 'File' is empty:
    - Generate a unique random *.html name that does not exist on disk and create it.
- If any new files were generated for rows with empty 'File', the CSV is updated in place
  with those new filenames (atomic write).

CSV columns expected: URL (required), File (optional)
"""

import sys
import os
import csv
import string
import secrets
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd


CSV_PATH = Path("bin/redirects.csv")
OUTPUT_DIR = Path(".")  # change to Path("out") if you want a subfolder
HTML_LANG = "da"


def generate_random_string(length: int = 7) -> str:
    """Generate a random string (a–z, 0–9), length=7."""
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def ensure_html_ext(name: str) -> str:
    """Ensure the filename ends with .html (adds it if missing)."""
    name = name.strip()
    if not name:
        return name
    return name if name.lower().endswith(".html") else f"{name}.html"


def unique_random_html_name(
    existing_names_on_disk: set[str], used_in_run: set[str]
) -> str:
    """Return a unique random filename ending with .html not colliding on disk or in this run."""
    while True:
        candidate = f"{generate_random_string()}.html"
        if candidate not in used_in_run and candidate not in existing_names_on_disk:
            return candidate


def generate_html(file_path: Path, url: str) -> None:
    html_content = f"""<!DOCTYPE html>
<html lang="{HTML_LANG}">
    <head>
        <meta charset="utf-8">
        <script>window.location.href = "{url}";</script>
        <meta name="robots" content="noindex, nofollow">
    </head>
    <body>
        <noscript>
            <meta http-equiv="refresh" content="0;url={url}">
        </noscript>
    </body>
</html>"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(html_content, encoding="utf-8")


def atomic_overwrite_csv(df: pd.DataFrame, path: Path) -> None:
    """
    Atomically overwrite CSV at `path` with DataFrame `df`, preserving UTF-8 and no index.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=str(path.parent), newline="") as tmp:
        tmp_path = Path(tmp.name)
        df.to_csv(tmp_path, index=False, encoding="utf-8", quoting=csv.QUOTE_MINIMAL)
    os.replace(tmp_path, path)  # atomic on most platforms


def main() -> int:
    if not CSV_PATH.exists():
        print(f"CSV not found: {CSV_PATH}", file=sys.stderr)
        return 1

    try:
        df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        return 1

    # Ensure expected columns exist (do not drop other columns if present)
    if "URL" not in df.columns:
        df["URL"] = ""
    if "File" not in df.columns:
        df["File"] = ""

    # Normalize
    df["URL"] = df["URL"].astype(str).str.strip()
    df["File"] = df["File"].astype(str).str.strip()

    # Build a set of existing filenames on disk (in OUTPUT_DIR) to avoid collisions.
    # Only consider .html files to match our output domain.
    existing_on_disk = {p.name for p in OUTPUT_DIR.glob("*.html")}

    # Track names used/generated in this run to prevent duplicates.
    used_in_run: set[str] = set(
        name for name in df["File"].map(ensure_html_ext) if name
    )

    generated = 0
    skipped_no_url = 0
    skipped_exists = 0

    # Track which rows were assigned a new file (so we can write them back to CSV)
    assigned_files: dict[int, str] = {}

    for idx, row in df.iterrows():
        url = row["URL"]
        if not url:
            print(
                f"Skipping row without URL at index {idx}: {row.to_dict()}",
                file=sys.stderr,
            )
            skipped_no_url += 1
            continue

        provided_name = row["File"]
        file_name = ensure_html_ext(provided_name) if provided_name else ""

        if file_name:
            # Provided file name; do not overwrite if it exists.
            file_path = OUTPUT_DIR / file_name
            if file_path.exists():
                print(f"Exists, skipping: {file_name}")
                skipped_exists += 1
                # Even if it didn't have .html before, do not rewrite CSV unless we actually generated a new file.
                # Normalize in-memory so future rows avoid collisions.
                used_in_run.add(file_name)
                continue
            else:
                # Ensure we don't collide with other rows in this run or other files on disk.
                while file_name in used_in_run or file_name in existing_on_disk:
                    file_name = unique_random_html_name(existing_on_disk, used_in_run)
                file_path = OUTPUT_DIR / file_name
        else:
            # No file provided — generate a unique random one
            file_name = unique_random_html_name(existing_on_disk, used_in_run)
            file_path = OUTPUT_DIR / file_name
            assigned_files[idx] = file_name  # remember to write back to CSV

        try:
            generate_html(file_path, url)
            used_in_run.add(file_name)
            existing_on_disk.add(file_name)
            print(f"Created: {file_name} -> {url}")
            generated += 1

            # If a provided name was missing the .html suffix, we didn't "generate" a new random name;
            # we simply normalized. We do NOT write that back unless it was missing entirely.
            # Only rows in assigned_files (initially empty File) will be persisted back.

        except Exception as e:
            print(f"Failed to write {file_name}: {e}", file=sys.stderr)

    # If any rows received a newly generated filename, update the CSV atomically.
    if assigned_files:
        for idx, new_name in assigned_files.items():
            df.at[idx, "File"] = new_name
        try:
            atomic_overwrite_csv(df, CSV_PATH)
            print(
                f"\nCSV updated with {len(assigned_files)} new file name(s): {CSV_PATH}"
            )
        except Exception as e:
            print(
                f"\nWarning: failed to update CSV with new files: {e}", file=sys.stderr
            )

    print(
        f"\nSummary:\n"
        f"  Created files: {generated}\n"
        f"  Skipped (no URL): {skipped_no_url}\n"
        f"  Skipped (already exists): {skipped_exists}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
