from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI(
    title="Job Intelligent App",
    description="API de matching CV / Offres d'emploi en France",
    version="0.1.0"
)

UPLOAD_DIR = "./app/tmp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
