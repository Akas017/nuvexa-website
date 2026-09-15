from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes.contact import router as contact_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NUVEXA API",
    description="Backend API for the NUVEXA website",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(contact_router)


@app.get("/")
def root():
    return {
        "message": "NUVEXA API is running",
        "status": "healthy",
    }