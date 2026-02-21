from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional
from app.services.job_search_service import JobSearchService
from app.services.france_travail_source import FranceTravailSource
import asyncio

app = FastAPI(
    title="Job Intelligent App",
    description="API de matching CV / Offres d'emploi en France",
    version="0.1.0"
)

UPLOAD_DIR = "./app/tmp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# CORS pour autoriser le frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenue sur Job Intelligent App API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload-cv")
def upload_cv(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    return {"filename": file.filename, "saved_path": file_location, "status": "uploaded"}

@app.post("/upload-cv-and-search")
def upload_cv_and_search(file: UploadFile = File(...), keywords: Optional[str] = Form(None)):
    # 1. Sauvegarde du CV
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    # 2. Vérification des mots-clés
    if not keywords or not keywords.strip():
        return JSONResponse(status_code=400, content={"error": "Veuillez entrer des mots-clés pour la recherche."})
    # 3. Recherche d'offres (uniquement si CV ET mots-clés)
    job_service = JobSearchService()
    job_service.add_source(FranceTravailSource())
    # On split les mots-clés utilisateur (par virgule ou espace)
    user_keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    if not user_keywords:
        user_keywords = [k.strip() for k in keywords.split() if k.strip()]
    # Recherche asynchrone
    offers = asyncio.run(job_service.search_all(user_keywords, limit=20))
    return {"filename": file.filename, "saved_path": file_location, "user_keywords": user_keywords, "offers": offers}
