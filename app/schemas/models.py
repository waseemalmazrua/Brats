# app/schemas/models.py
from pydantic import BaseModel
from typing import Any, Dict, Optional


class InputData(BaseModel):
    folder_path: str
    case_id: Optional[str] = None


class OutputData(BaseModel):
    report: Dict[str, Any]
    seg_path: str
    json_path: str