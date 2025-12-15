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

@app.on_event("startup")
async def startup_event():
    print("🚀 Triggering initial news ingestion on startup...")
    try:
        from src.api.routers.news import run_ingestion_task
        # Run directly (blocking) or in background? 
        # For startup, blocking safely ensures data is ready before first request.
        # But for faster boot, we can background it. 
        # Given Railway 512MB limit, safer to background it so health check passes fast.
        import threading
        t = threading.Thread(target=run_ingestion_task)
        t.start()
        print("✅ Background ingestion thread started.")
    except Exception as e:
        print(f"❌ Startup ingestion failed: {e}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
