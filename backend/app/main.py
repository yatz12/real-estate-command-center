from fastapi import FastAPI
from app.api.routes.analytics import router as analytics_router

app = FastAPI(
    title="Investor's Saheli AI",
    version="0.1.0",
)

app.include_router(analytics_router)

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "investors-saheli-ai",
        "version": "0.1.0",
    }
