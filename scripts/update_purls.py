#!/usr/bin/env python3
"""
Generate/refresh simple HTML redirect files from data/redirects.csv using pandas.

Behavior changes (idempotent writes):
- For each row with a URL, (re)generate the target HTML content.
- If the file doesn't exist, create it.
- If it exists but content differs, atomically replace it (update).
- If it exists and content matches, leave it untouched (unchanged).

Other behaviors preserved:
- Rows without a URL are skipped (warned).
- If 'File' is provided:
    - Ensure it ends with .html.
    - Avoid duplicate filenames within the same run (warn + skip duplicates).
- If 'File' is empty:
    - Generate a unique random *.html name that does not exist on disk
      and is not used elsewhere in the CSV/run, then create it.
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
from tempfile import mkstemp
import os

import pandas as pd

CSV_PATH = Path("data/redirects.csv")
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


def html_content_for(url: str) -> str:
    return f"""<!DOCTYPE html>
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


def write_if_changed(file_path: Path, content: str) -> str:
    """
    Atomically write `content` to `file_path` iff the file doesn't exist
    or its contents differ. Preserve existing file mode if present;
    otherwise default to 0o644. Returns: "created" | "updated" | "unchanged".
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    existed = file_path.exists()
    existing_mode = None

    if existed:
        try:
            old = file_path.read_text(encoding="utf-8")
            if old == content:
                return "unchanged"
        except Exception:
            pass
        try:
            existing_mode = file_path.stat().st_mode & 0o777
        except Exception:
            pass

    # Create a temp file in the same directory
    fd, tmp_name = mkstemp(dir=str(file_path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as tmp:
            tmp.write(content)
            tmp.flush()
            os.fsync(tmp.fileno())

        # Preserve original perms or default to 0644
        os.chmod(tmp_name, existing_mode if existing_mode is not None else 0o644)

        # Atomic replace
        os.replace(tmp_name, file_path)
    finally:
        # If replace failed, ensure temp file is removed
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass

    return "updated" if existed else "created"


def atomic_overwrite_csv(df: pd.DataFrame, path: Path) -> None:
    """Atomically overwrite CSV at `path` with DataFrame `df`, preserving UTF-8 and no index."""
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

    # Snapshot of existing .html files on disk
    existing_on_disk = {p.name for p in OUTPUT_DIR.glob("*.html")}

    # Track names used in this run (after normalization), to catch duplicates in CSV
    used_in_run: set[str] = set(
        name for name in df["File"].map(ensure_html_ext) if name
    )

    created = 0
    updated = 0
    unchanged = 0
    skipped_no_url = 0
    skipped_duplicate_name = 0

    # rows that were assigned a new filename (so we can write back to CSV)
    assigned_files: dict[int, str] = {}

    seen_names: set[str] = set()

    for idx, row in df.iterrows():
        url = row["URL"]
        if not url:
            print(f"Skipping row without URL at index {idx}: {row.to_dict()}", file=sys.stderr)
            skipped_no_url += 1
            continue

        provided_name = row["File"]
        file_name = ensure_html_ext(provided_name) if provided_name else ""

        if file_name:
            # detect duplicates inside the CSV for the current run
            if file_name in seen_names:
                print(f"Duplicate file name in CSV for index {idx}: {file_name}. Skipping this row.", file=sys.stderr)
                skipped_duplicate_name += 1
                continue

            # If the provided name collides with a different file on disk,
            # we still honor it — we'll just update that file. This preserves stable URLs.
            file_path = OUTPUT_DIR / file_name
        else:
            # No file provided — generate a unique random one
            file_name = unique_random_html_name(existing_on_disk, used_in_run | seen_names)
            file_path = OUTPUT_DIR / file_name
            assigned_files[idx] = file_name  # remember to write back to CSV

        seen_names.add(file_name)

        try:
            content = html_content_for(url)
            result = write_if_changed(file_path, content)
            if result == "created":
                print(f"Created:   {file_name} -> {url}")
                created += 1
                existing_on_disk.add(file_name)
            elif result == "updated":
                print(f"Updated:   {file_name} -> {url}")
                updated += 1
            else:
                print(f"Unchanged: {file_name} -> {url}")
                unchanged += 1
        except Exception as e:
            print(f"Failed to write {file_name}: {e}", file=sys.stderr)

    # If any rows received a newly generated filename, update the CSV atomically.
    if assigned_files:
        for idx, new_name in assigned_files.items():
            df.at[idx, "File"] = new_name
        try:
            atomic_overwrite_csv(df, CSV_PATH)
            print(f"\nCSV updated with {len(assigned_files)} new file name(s): {CSV_PATH}")
        except Exception as e:
            print(f"\nWarning: failed to update CSV with new files: {e}", file=sys.stderr)

    print(
        f"\nSummary:\n"
        f"  Created files: {created}\n"
        f"  Updated files: {updated}\n"
        f"  Unchanged:     {unchanged}\n"
        f"  Skipped (no URL):           {skipped_no_url}\n"
        f"  Skipped (duplicate name):   {skipped_duplicate_name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
