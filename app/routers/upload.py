from google.cloud import storage
from google.auth import impersonated_credentials
import google.auth
import google.auth.transport.requests
from datetime import timedelta
from fastapi import APIRouter, Depends
from app.core.security import verify_token

router = APIRouter(prefix="/upload", tags=["upload"])


def get_credentials():
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials


@router.get("/signed-url")
def get_signed_url(filename: str, modality: str, user=Depends(verify_token)):
    credentials = get_credentials()
    client = storage.Client(credentials=credentials)
    bucket = client.bucket("brats-uploads")
    blob_name = f"uploads/{user['sub']}/{modality}/{filename}"
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=15),
        method="PUT",
        content_type="application/octet-stream",
        service_account_email="850442724763-compute@developer.gserviceaccount.com",
        access_token=credentials.token,
    )
    return {"url": url, "gcs_path": f"gs://brats-uploads/{blob_name}"}