#!/usr/bin/env python3
"""
convert.py — Batch convert all .pub files in Proud_pets_PUB_files/ to plain text.
Outputs flat .txt files into output/ at the project root.

Strategy:
  1. soffice --headless converts each .pub -> .pdf  (LibreOffice Draw supports PDF export)
  2. pypdf extracts the plain text from each PDF
  3. The intermediate .pdf is deleted

Requires:
  - LibreOffice (soffice):  brew install --cask libreoffice
  - pypdf:                  pip3 install pypdf
"""

import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

from pypdf import PdfReader

INPUT_DIR = Path(__file__).parent / "Proud_pets_PUB_files"
OUTPUT_DIR = Path(__file__).parent / "output"


def check_soffice():
    if not shutil.which("soffice"):
        print("ERROR: 'soffice' (LibreOffice) not found in PATH.")
        print("Install it with:  brew install --cask libreoffice")
        sys.exit(1)


def pub_to_text(pub_file: Path, tmp_dir: Path) -> str:
    """Convert a .pub file to plain text via an intermediate PDF."""
    # Step 1: pub -> pdf
    result = subprocess.run(
        [
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(tmp_dir),
            str(pub_file),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"soffice failed: {result.stderr.strip()}")

    pdf_path = tmp_dir / (pub_file.stem + ".pdf")
    if not pdf_path.exists():
        raise RuntimeError(f"Expected PDF not found: {pdf_path}")

    # Step 2: pdf -> text via pypdf
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n\n".join(pages).strip()

    pdf_path.unlink()  # clean up intermediate PDF
    return text


def main():
    check_soffice()

    pub_files = sorted(INPUT_DIR.rglob("*.pub"))
    if not pub_files:
        print(f"No .pub files found under {INPUT_DIR}")
        sys.exit(0)

    OUTPUT_DIR.mkdir(exist_ok=True)
    total = len(pub_files)
    failed = []

    print(f"Found {total} .pub files. Converting to {OUTPUT_DIR}/\n")

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for i, pub_file in enumerate(pub_files, 1):
            print(f"[{i}/{total}] {pub_file.name} ...", end=" ", flush=True)
            try:
                text = pub_to_text(pub_file, tmp_dir)
                out_file = OUTPUT_DIR / (pub_file.stem + ".txt")
                out_file.write_text(text, encoding="utf-8")
                print("OK")
            except Exception as e:
                print(f"FAILED ({e})")
                failed.append(pub_file.name)

    print(f"\nDone. {total - len(failed)}/{total} files converted to {OUTPUT_DIR}/")

    if failed:
        print(f"\nFailed ({len(failed)}):")
        for name in failed:
            print(f"  {name}")


if __name__ == "__main__":
    main()
