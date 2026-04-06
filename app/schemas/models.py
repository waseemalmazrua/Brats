# app/schemas/models.py
from typing import Any

from pydantic import BaseModel


class InputData(BaseModel):
    folder_path: str
    case_id: str | None = None


class OutputData(BaseModel):
    report: dict[str, Any]
    seg_path: str
    json_path: str