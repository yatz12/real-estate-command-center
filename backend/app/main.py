from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.analytics import router as analytics_router
from app.api.routes.upload import router as upload_router
from app.db.database import engine
from app.models.post import Base

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Investor's Saheli AI",
    version="0.1.0",
)

# --- CORS CONFIGURATION ---
# This allows the Next.js frontend (port 3000) to talk to the FastAPI backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analytics_router)
app.include_router(upload_router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "investors-saheli-ai",
        "version": "0.1.0",
    }
