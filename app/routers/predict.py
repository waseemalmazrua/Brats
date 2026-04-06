import base64
import time
import traceback

import httpx
from fastapi import APIRouter, File, HTTPException, UploadFile
from prometheus_client import Counter, Histogram

from app.core.config import settings
from app.core.prediction_services import get_cached_prediction, set_cached_prediction
from app.core.utils import explain_prediction

router = APIRouter(prefix="/predict", tags=["predict"])

BENTO_URL = settings.BENTO_URL

prediction_counter = Counter("predictions_total", "Total number of prediction requests")
prediction_errors = Counter("prediction_errors_total", "Total number of prediction errors")
prediction_latency = Histogram("prediction_latency_seconds", "Time spent on prediction endpoint")


def clean_json(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8")
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_json(i) for i in obj]
    return obj


@router.post("/")
async def predict(
    t1: UploadFile = File(...),
    t1ce: UploadFile = File(...),
    t2: UploadFile = File(...),
    flair: UploadFile = File(...)
):
    prediction_counter.inc()
    start_time = time.time()

    try:
        files_bytes = {
            "t1": await t1.read(),
            "t1ce": await t1ce.read(),
            "t2": await t2.read(),
            "flair": await flair.read(),
        }

        cached = get_cached_prediction(files_bytes)
        if cached:
            result = cached
        else:
            # encode كـ base64
            payload = {
                "t1": base64.b64encode(files_bytes["t1"]).decode("utf-8"),
                "t1ce": base64.b64encode(files_bytes["t1ce"]).decode("utf-8"),
                "t2": base64.b64encode(files_bytes["t2"]).decode("utf-8"),
                "flair": base64.b64encode(files_bytes["flair"]).decode("utf-8"),
            }

            async with httpx.AsyncClient(timeout=300) as client:
                response = await client.post(
                    f"{BENTO_URL}/predict",
                    json=payload
                )

            if response.status_code != 200:
                prediction_errors.inc()
                raise HTTPException(
                    status_code=500,
                    detail=f"BentoML error: {response.text}"
                )

            result = clean_json(response.json())
            set_cached_prediction(files_bytes, result)

        explanation = await explain_prediction(result)

        return {
            "prediction": result,
            "explanation": explanation
        }

    except Exception as e:
            prediction_errors.inc()
            print("❌ FastAPI Error:", traceback.format_exc())  # أضف هذا
            raise HTTPException(status_code=500, detail=str(e))

    finally:
        duration = time.time() - start_time
        prediction_latency.observe(duration)