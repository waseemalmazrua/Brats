impory bentoml
import mlflow.pyfunc

from core.config import settings

def export():
    print("loading model from mlflow...")
    print(f"URI : {settings.MLFLOW_MODEL_URI}")

    model = mlflow.pyfunc.load_model(settings.MLFLOW_MODEL_URI)


print("saving model to bentoml...")
    bentoml.mlflow.save_model(settings.BENTO_MODEL_NAME, model)

    print("model saved to bentoml")
   
if __name__ = "__main__":
    export()