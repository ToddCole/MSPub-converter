# MSPub Converter

A simple one-shot batch converter that extracts plain text from Microsoft Publisher (`.pub`) files.

## What it does

Reads all `.pub` files in the `Proud_pets_PUB_files/` folder (including the `FRANKS_SPECIALS/` subfolder) and converts each one to a plain `.txt` file with all Publisher formatting stripped. Output files are written flat into an `output/` folder at the project root.

## Requirements

- **LibreOffice** — used to convert `.pub` → PDF headlessly
  ```
  brew install --cask libreoffice
  ```
- **pypdf** — used to extract text from the intermediate PDF
  ```
  pip3 install pypdf
  ```

## Usage

```bash
python3 convert.py
```

Progress is printed for each file. Any failures are reported at the end without stopping the rest of the run.

## Output

- 112 `.txt` files land in `output/` (not tracked by git)
- File names match the original `.pub` names (e.g. `GoldenRetriever.pub` → `GoldenRetriever.txt`)
- The `output/` folder is created automatically if it doesn't exist

## How it works

1. For each `.pub` file, `soffice --headless` converts it to PDF in a temporary directory (Publisher files open as LibreOffice Draw documents, which support PDF export)
2. `pypdf` extracts the text from the PDF
3. The intermediate PDF is deleted
4. The plain text is written to `output/<name>.txt`
