from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from src.api.routers import analyze, news

app = FastAPI(title="FinVani API")

# Configure CORS
origins = [
    "http://localhost:3000",
]

# Add production origins from environment variable
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    origins.extend([origin.strip() for origin in env_origins.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(analyze.router)
app.include_router(news.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
