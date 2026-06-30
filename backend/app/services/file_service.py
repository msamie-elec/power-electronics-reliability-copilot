from datetime import datetime
from typing import Any

from fastapi import UploadFile

from app.config import UPLOAD_DIR

UPLOAD_DIR.mkdir(exist_ok=True)


async def save_uploaded_file(file: UploadFile) -> dict[str, Any]:
    destination = UPLOAD_DIR / file.filename

    content = await file.read()
    destination.write_bytes(content)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
        "uploaded_at": datetime.now().isoformat(timespec="seconds"),
    }


def list_uploaded_documents() -> list[dict[str, Any]]:
    documents = []

    for path in UPLOAD_DIR.iterdir():
        if path.is_file() and path.name != ".gitkeep":
            documents.append(
                {
                    "filename": path.name,
                    "size_bytes": path.stat().st_size,
                    "uploaded_at": datetime.fromtimestamp(
                        path.stat().st_mtime
                    ).isoformat(timespec="seconds"),
                }
            )

    return documents