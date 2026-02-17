from fastapi import FastAPI

app = FastAPI(
    title="Job Intelligent App",
    description="API de matching CV / Offres d'emploi en France",
    version="0.1.0"
)


@app.get("/")
def root():
    return {"message": "Bienvenue sur Job Intelligent App API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
