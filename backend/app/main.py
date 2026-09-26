from fastapi import FastAPI
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

app.include_router(analytics_router)
app.include_router(upload_router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "investors-saheli-ai",
        "version": "0.1.0",
    }
