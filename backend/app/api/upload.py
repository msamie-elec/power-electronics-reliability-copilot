from typing import List

from fastapi import APIRouter, File, UploadFile

from app.services.file_service import save_uploaded_file

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("")
async def upload_files(files: List[UploadFile] = File(...)) -> dict:
    saved_files = []

    for file in files:
        saved_file = await save_uploaded_file(file)
        saved_files.append(saved_file)

    return {"uploaded_files": saved_files}