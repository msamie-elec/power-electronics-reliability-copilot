from pathlib import Path
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.file_service import save_uploaded_file


ALLOWED_FILE_EXTENSIONS = {".pdf", ".txt", ".csv"}

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("")
async def upload_files(files: List[UploadFile] = File(...)) -> dict:
    saved_files = []

    for file in files:
        file_extension = Path(file.filename).suffix.lower()

        if file_extension not in ALLOWED_FILE_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Unsupported file type: {file_extension}. "
                    "Allowed types: PDF, TXT, CSV."
                ),
            )

        saved_file = await save_uploaded_file(file)
        saved_files.append(saved_file)

    return {"uploaded_files": saved_files}