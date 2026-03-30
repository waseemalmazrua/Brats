import bentoml
import json
import nibabel as nib
import numpy as np
from pathlib import Path
from typing import Optional
import torch
import mlflow.pyfunc

from app.core.config import settings
from app.core.modality_detector import (
    detect_modalities_from_folder,
    validate_modalities,
)
from app.schemas.models import OutputData


@bentoml.service(
    traffic={"timeout": 300}
)
class BratsService:

    def __init__(self):
        self.model = mlflow.pyfunc.load_model(
            settings.MLFLOW_MODEL_URI
        )

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # 🔥 انتبه: pyfunc model غالبًا ما يدعم .to()
        if hasattr(self.model, "to"):
            self.model.to(self.device)

        if hasattr(self.model, "eval"):
            self.model.eval()

        print(f"🚀 Model running on: {self.device}")

    @bentoml.api()
    def predict(self, folder_path: str, case_id: Optional[str] = None) -> OutputData:

        folder = Path(folder_path)

        if not folder.exists():
            raise ValueError(f"المسار غير موجود: {folder}")
        if not folder.is_dir():
            raise ValueError(f"المسار ليس folder: {folder}")

        case_id = case_id or folder.name

        modalities = detect_modalities_from_folder(str(folder))
        validate_modalities(modalities)

        image_paths = [
            modalities["t1"],
            modalities["t1ce"],
            modalities["t2"],
            modalities["flair"],
        ]

        # 🔥 inference
        with torch.no_grad():
            result = self.model.predict({"image": image_paths})

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        json_path = output_dir / f"{case_id}_report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result["report"], f, indent=4, ensure_ascii=False)

        ref_img   = nib.load(image_paths[1])
        seg_array = np.asarray(result["segmentation"]).astype(np.uint8)
        seg_img   = nib.Nifti1Image(seg_array, affine=ref_img.affine, header=ref_img.header)

        seg_path  = output_dir / f"{case_id}_segmentation.nii.gz"
        nib.save(seg_img, seg_path)

        return OutputData(
            report=result["report"],
            seg_path=str(seg_path),
            json_path=str(json_path),
        )