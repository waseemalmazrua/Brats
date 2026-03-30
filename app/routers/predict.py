from fastapi import APIRouter, HTTPException
import httpx
import time

from app.core.config import settings
from app.schemas.models import InputData
from app.core.utils import explain_prediction

from prometheus_client import Counter, Histogram
from app.core.prediction_services import get_cached_prediction, set_cached_prediction

router = APIRouter(prefix="/predict", tags=["predict"])

BENTO_URL = settings.BENTO_URL


# 🔢 عدد الطلبات
prediction_counter = Counter(
    "predictions_total",
    "Total number of prediction requests"
)

# ❌ عدد الأخطاء
prediction_errors = Counter(
    "prediction_errors_total",
    "Total number of prediction errors"
)

# ⏱️ وقت التنفيذ
prediction_latency = Histogram(
    "prediction_latency_seconds",
    "Time spent on prediction endpoint"
)



@router.post("/")
async def predict(request: InputData):

    prediction_counter.inc()
    start_time = time.time()

    data = {
        "folder_path": request.folder_path,
        "case_id": request.case_id
    }

    try:
        # 🧠 1. Check cache
        cached = get_cached_prediction(data)
        if cached:
            result = cached

        else:
            # 🚀 2. Call Bento
            async with httpx.AsyncClient(timeout=300) as client:
                response = await client.post(
                    f"{BENTO_URL}/predict",
                    json=data
                )

            if response.status_code != 200:
                prediction_errors.inc()
                raise HTTPException(status_code=500, detail="BentoML error")

            result = response.json()

            # 💾 3. Save cache
            set_cached_prediction(data, result)

        # 🧠 4. Explanation
        explanation = await explain_prediction(result)

        return {
            "prediction": result,
            "explanation": explanation
        }

    except Exception:
        prediction_errors.inc()
        raise HTTPException(status_code=500, detail="Prediction failed")

    finally:
        duration = time.time() - start_time
        prediction_latency.observe(duration)