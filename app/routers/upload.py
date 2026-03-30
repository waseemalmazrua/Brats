from fastapi import APIRouter, UploadFile, File
import shutil
import uuid
from pathlib import Path

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ACCEPTED = {".nii", ".gz"}

@router.post("/")
async def upload_files(
    t1: UploadFile = File(...),
    t1ce: UploadFile = File(...),
    t2: UploadFile = File(...),
    flair: UploadFile = File(...),
):
    case_id = str(uuid.uuid4())[:8]
    folder = UPLOAD_DIR / case_id
    folder.mkdir(parents=True, exist_ok=True)

    for file in [t1, t1ce, t2, flair]:
        dest = folder / file.filename
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)

    return {"folder_path": str(folder), "case_id": case_id}