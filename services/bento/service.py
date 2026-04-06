import base64
import bentoml
import json
import nibabel as nib
import numpy as np
from pathlib import Path
import torch
import mlflow.pyfunc
import tempfile

from app.core.config import settings
from app.schemas.models import OutputData


def clean_bytes(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8")
    if isinstance(obj, dict):
        return {k: clean_bytes(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_bytes(i) for i in obj]
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


@bentoml.service(traffic={"timeout": 300})
class BratsService:

    def __init__(self):
        self.model = mlflow.pyfunc.load_model(settings.MLFLOW_MODEL_URI)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"🚀 Model running on: {self.device}")

    @bentoml.api()
    def predict(self, t1: str, t1ce: str, t2: str, flair: str) -> OutputData:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)

                t1_path = tmp_path / "t1.nii"
                t1ce_path = tmp_path / "t1ce.nii"
                t2_path = tmp_path / "t2.nii"
                flair_path = tmp_path / "flair.nii"

                t1_path.write_bytes(base64.b64decode(t1))
                t1ce_path.write_bytes(base64.b64decode(t1ce))
                t2_path.write_bytes(base64.b64decode(t2))
                flair_path.write_bytes(base64.b64decode(flair))

                print(f"✅ t1: {t1_path.stat().st_size} bytes")
                print(f"✅ t1ce: {t1ce_path.stat().st_size} bytes")
                print(f"✅ t2: {t2_path.stat().st_size} bytes")
                print(f"✅ flair: {flair_path.stat().st_size} bytes")

                image_paths = [
                    str(t1_path),
                    str(t1ce_path),
                    str(t2_path),
                    str(flair_path),
                ]

                result = self.model.predict({"image": image_paths})

                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)

                case_id = "temp_case"
                clean_report = clean_bytes(result["report"])

                json_path = output_dir / f"{case_id}_report.json"
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(clean_report, f, indent=4, ensure_ascii=False)

                ref_img = nib.load(image_paths[1])
                seg_array = np.asarray(result["segmentation"]).astype(np.uint8)
                seg_img = nib.Nifti1Image(seg_array, affine=ref_img.affine, header=ref_img.header)

                seg_path = output_dir / f"{case_id}_segmentation.nii.gz"
                nib.save(seg_img, seg_path)

                return OutputData(
                    report=clean_report,
                    seg_path=str(seg_path),
                    json_path=str(json_path),
                )

        except Exception as e:
            print("❌ Bento Error:", str(e))
            raise