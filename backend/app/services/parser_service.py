import json
from datetime import datetime
from pathlib import Path
from typing import Any

import fitz

from app.config import DOCUMENTS_DIR, METADATA_DIR

DOCUMENTS_DIR.mkdir(exist_ok=True)
METADATA_DIR.mkdir(exist_ok=True)


def extract_text_from_pdf(pdf_path: Path) -> dict[str, Any]:
    document = fitz.open(pdf_path)
    extracted_pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")
        extracted_pages.append(
            {
                "page_number": page_number,
                "text": text,
                "character_count": len(text),
            }
        )

    full_text = "\n\n".join(
        f"[Page {page['page_number']}]\n{page['text']}"
        for page in extracted_pages
    )

    output_text_path = DOCUMENTS_DIR / f"{pdf_path.stem}.txt"
    output_metadata_path = METADATA_DIR / f"{pdf_path.stem}.json"

    output_text_path.write_text(full_text, encoding="utf-8")

    metadata = {
        "source_filename": pdf_path.name,
        "text_filename": output_text_path.name,
        "page_count": len(extracted_pages),
        "character_count": len(full_text),
        "processed_at": datetime.now().isoformat(timespec="seconds"),
        "pages": [
            {
                "page_number": page["page_number"],
                "character_count": page["character_count"],
            }
            for page in extracted_pages
        ],
    }

    output_metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )

    document.close()

    return metadata