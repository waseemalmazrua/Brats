<div align="center">

# 🧠 Brats-3D — Brain Tumor MRI Analysis Platform

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&pause=1000&color=00B4D8&center=true&vCenter=true&width=500&lines=AI-Powered+Brain+Tumor+Segmentation;3D+UNet+%7C+BraTS2020+%7C+Full-Stack+MLOps" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![BentoML](https://img.shields.io/badge/BentoML-000000?style=for-the-badge&logo=bentoml&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

<br/>

![Domain](https://img.shields.io/badge/Domain-Medical%20Imaging-red?style=flat-square)
![Framework](https://img.shields.io/badge/Framework-3D%20UNet-blue?style=flat-square)
![Dataset](https://img.shields.io/badge/Dataset-BraTS2020-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Live%20%F0%9F%9F%A2-brightgreen?style=flat-square)
![Live](https://img.shields.io/badge/Live-brats--3d.web.app-00B4D8?style=flat-square&logo=firebase)

</div>

---
link : https://brats-3d.web.app/

An end-to-end AI-powered clinical platform for automated brain tumor segmentation using multi-modal MRI scans, built on the BraTS2020 benchmark dataset. The system accepts four MRI modalities as input and returns a detailed segmentation report identifying tumor sub-regions with clinical significance.

---

## Dataset — BraTS2020

The Brain Tumor Segmentation (BraTS) dataset consists of multi-institutional, pre-operative MRI scans from 19 institutions. All scans are co-registered to a standard anatomical template, resampled to 1mm³ isotropic resolution, and skull-stripped.

### Input Modalities

| Modality | Full Name | Clinical Role |
|---|---|---|
| T1 | T1-weighted (native) | Baseline brain anatomy, identifies normal tissue structure |
| T1CE (T1Gd) | T1-weighted post-contrast | Highlights active tumor using gadolinium contrast agent |
| T2 | T2-weighted | Shows edema and infiltration, high signal in fluid regions |
| FLAIR | T2 Fluid Attenuated Inversion Recovery | Suppresses CSF signal, best for peritumoral edema detection |

### Segmentation Classes

| Label | Class | Name | Description |
|---|---|---|---|
| 1 | NCR/NET | Necrotic and Non-Enhancing Tumor Core | Dead tissue at the center of the tumor. Appears dark on T1CE. Represents the oldest, most necrotic part of the tumor mass. |
| 2 | ED | Peritumoral Edema | Swelling around the tumor caused by fluid leakage. Best visible on T2/FLAIR. Does not contain active tumor cells but causes significant intracranial pressure. |
| 4 | ET | GD-Enhancing Tumor | Actively growing, invasive tumor region. Lights up on T1CE due to blood-brain barrier breakdown. Most clinically significant region for treatment planning and surgery. |

### Composite Tumor Regions (used in evaluation)

| Region | Composed of | Clinical Meaning |
|---|---|---|
| Whole Tumor (WT) | ET + ED + NCR/NET | Total tumor extent including all affected tissue |
| Tumor Core (TC) | ET + NCR/NET | The core mass excluding surrounding edema |
| Enhancing Tumor (ET) | ET only | Active tumor, used for surgical and radiation targeting |

---

## Model Performance

| Metric | Value | Description |
|---|---|---|
| Train Loss | 0.3547 | DiceCE combined loss on training set |
| Val Mean Dice | 0.7155 | Average Dice score across all three tumor classes |
| Val Dice — Class 1 (NCR/NET) | 0.8073 | Segmentation accuracy for necrotic core |
| Val Dice — Class 2 (ED) | 0.8434 | Segmentation accuracy for peritumoral edema |
| Val Dice — Class 3 (ET) | 0.8261 | Segmentation accuracy for enhancing tumor |

> Dice Score measures overlap between predicted and ground truth segmentation. A score of 1.0 means perfect overlap.

### Training Configuration

| Parameter | Value |
|---|---|
| Architecture | 3D UNet |
| Dataset | BraTS2020 |
| In Channels | 4 (T1, T1CE, T2, FLAIR) |
| Out Channels | 4 (background + 3 classes) |
| Optimizer | AdamW |
| Loss Function | DiceCELoss |
| Learning Rate | 0.0001 |
| Batch Size | 2 |
| Max Epochs | 100 |
| Early Stopping | Patience 15 |
| Device | CUDA |

---

## System Architecture

```
Frontend (React + Vite)
        ↓ Auth0 JWT
FastAPI Backend  ──────────────────────→  Cloud Run (us-central1)
        ↓                                          ↓
GCS Signed URL                          Neon PostgreSQL
        ↓
Google Cloud Storage (brats-uploads)
        ↓ GCS paths
BentoML Inference Service  ────────────→  Cloud Run (us-central1)
        ↓
   3D UNet Model
        ↓
Segmentation Report + NIfTI Output
```

---

## Tech Stack

**AI & ML**
- 3D UNet trained on BraTS2020
- BentoML for model serving and API
- MLflow for experiment tracking and model registry
- PyTorch with CUDA support

**Backend**
- FastAPI — async REST API
- Auth0 — JWT-based authentication
- SQLAlchemy + Alembic — ORM and database migrations
- Prometheus + Grafana — metrics and monitoring
- Redis — prediction result caching

**Infrastructure**
- Google Cloud Run — serverless container deployment
- Google Cloud Storage — large MRI file storage (bypasses 32MB Cloud Run limit)
- Neon PostgreSQL — serverless production database
- Firebase Hosting — frontend CDN deployment
- GitHub Actions — full CI/CD pipeline

---

## CI/CD Pipeline

Every push to `main` automatically triggers:

1. Spin up isolated PostgreSQL test container
2. Run full test suite with pytest
3. Run Alembic migrations against production Neon database
4. Build and push FastAPI Docker image to GCR
5. Build and push BentoML Docker image to GCR
6. Deploy FastAPI to Cloud Run
7. Deploy BentoML to Cloud Run
8. Build React frontend with production environment variables
9. Deploy frontend to Firebase Hosting

---

## File Upload Flow

Standard Cloud Run requests are limited to 32MB, which MRI NIfTI files easily exceed. The platform handles this with GCS signed URLs:

1. Frontend requests a signed upload URL from FastAPI
2. FastAPI generates a 15-minute PUT signed URL via GCS
3. Frontend uploads the file directly to GCS — bypassing Cloud Run entirely
4. Frontend sends only the GCS file paths to FastAPI for inference
5. BentoML downloads files from GCS, runs the 3D UNet, and returns results

---


---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| GET | `/upload/signed-url` | Yes | Get GCS signed URL for direct MRI file upload |
| POST | `/predict/` | Yes | Submit GCS file paths and run tumor segmentation |
| GET | `/users/me` | Yes | Get authenticated user profile |
| POST | `/login` | No | Auth0 token exchange |
| GET | `/metrics` | No | Prometheus metrics scrape endpoint |

---

## Author

Waseem Almazrua — [LinkedIn](https://www.linkedin.com/in/waseemalmazrua/)
