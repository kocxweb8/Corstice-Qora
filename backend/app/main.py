from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import projects, drawings, analysis, quantities, reports

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Qora API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(drawings.router, prefix="/api/drawings", tags=["Drawings"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(quantities.router, prefix="/api/quantities", tags=["Quantities"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])

@app.get("/")
def root():
    return {"message": "Qora API is running"}