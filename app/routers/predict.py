import time
import traceback

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from prometheus_client import Counter, Histogram

from app.core.config import settings
from app.core.prediction_services import get_cached_prediction, set_cached_prediction
from app.core.utils import explain_prediction

router = APIRouter(prefix="/predict", tags=["predict"])

BENTO_URL = settings.BENTO_URL

prediction_counter = Counter("predictions_total", "Total number of prediction requests")
prediction_errors = Counter("prediction_errors_total", "Total number of prediction errors")
prediction_latency = Histogram("prediction_latency_seconds", "Time spent on prediction endpoint")


class PredictRequest(BaseModel):
    t1: str
    t1ce: str
    t2: str
    flair: str


def clean_json(obj):
    if isinstance(obj, bytes):
        return obj.decode("utf-8")
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_json(i) for i in obj]
    return obj


@router.post("/")
async def predict(request: PredictRequest):
    prediction_counter.inc()
    start_time = time.time()

    try:
        cache_key = request.model_dump()
        cached = get_cached_prediction(cache_key)
        if cached:
            result = cached
        else:
            payload = {
                "t1": request.t1,
                "t1ce": request.t1ce,
                "t2": request.t2,
                "flair": request.flair,
            }

            async with httpx.AsyncClient(timeout=3600) as client:
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
            set_cached_prediction(cache_key, result)

        explanation = await explain_prediction(result)
        return {"prediction": result, "explanation": explanation}

    except Exception as e:
        prediction_errors.inc()
        print("❌ FastAPI Error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        duration = time.time() - start_time
        prediction_latency.observe(duration)