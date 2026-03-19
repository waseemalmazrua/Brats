# app/services/brats_service.py
import bentoml
import json
import nibabel as nib
import numpy as np
from pathlib import Path

from app.core.config import settings
from app.core.modality_detector import (
    detect_modalities_from_folder,
    validate_modalities,
)
from app.schemas.models import InputData, OutputData


@bentoml.service
class BratsService:

    def __init__(self):
        model_ref = bentoml.mlflow.get(settings.BENTOML_MODEL_TAG)
        self.model = model_ref.load_model()

    @bentoml.api
    def predict(self, data: InputData) -> OutputData:

        # ── 1. التحقق من المسار ──
        folder = Path(data.folder_path)

        if not folder.exists():
            raise ValueError(f"المسار غير موجود: {folder}")
        if not folder.is_dir():
            raise ValueError(f"المسار ليس folder: {folder}")

        case_id = data.case_id or folder.name

        # ── 2. اكتشاف الـ modalities تلقائياً ──
        modalities = detect_modalities_from_folder(str(folder))
        validate_modalities(modalities)

        image_paths = [
            modalities["t1"],
            modalities["t1ce"],
            modalities["t2"],
            modalities["flair"],
        ]

        # ── 3. تشغيل الموديل ──
        result = self.model.predict({"image": image_paths})

        # ── 4. حفظ النتائج ──
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # JSON report
        json_path = output_dir / f"{case_id}_report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result["report"], f, indent=4, ensure_ascii=False)

        # NIfTI segmentation — نفس الـ affine والـ header من T1 الأصلي
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