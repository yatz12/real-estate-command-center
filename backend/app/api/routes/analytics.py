from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.analytics_service import (
    get_overall_summary, 
    get_top_posts, 
    get_performance_by_format, 
    get_timeline_analytics
)

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
async def get_summary(db: Session = Depends(get_db)):
    return get_overall_summary(db)

@router.get("/top-posts")
async def get_top_posts_api(limit: int = 10, db: Session = Depends(get_db)):
    return get_top_posts(db, limit)

@router.get("/by-format")
async def get_format_performance(db: Session = Depends(get_db)):
    return get_performance_by_format(db)

@router.get("/timeline")
async def get_timeline(db: Session = Depends(get_db)):
    return get_timeline_analytics(db)
