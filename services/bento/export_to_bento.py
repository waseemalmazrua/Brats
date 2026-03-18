import bentoml
import mlflow.pyfunc
import mlflow

from app.core.config import settings

def export():
    print("loading model from mlflow...")
    print(f"URI : {settings.MLFLOW_MODEL_URI}")

    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

    model = mlflow.pyfunc.load_model(settings.MLFLOW_MODEL_URI)


    print("saving model to bentoml...")
    bentoml.mlflow.import_model(
    name=settings.BENTO_MODEL_NAME,
    model_uri=settings.MLFLOW_MODEL_URI,
)

    print("model saved to bentoml")
   
if __name__ == "__main__":
    export()