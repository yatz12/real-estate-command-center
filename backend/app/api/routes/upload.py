from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.csv_parser import parse_instagram_csv
from app.services.post_service import create_posts
from app.schemas.analytics import AnalysisSummary
import shutil
import os
import tempfile

router = APIRouter(prefix="/analytics", tags=["upload"])

@router.post("/analyse", response_model=AnalysisSummary)
async def analyse_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        # Parse and validate
        data = parse_instagram_csv(tmp_path)
        
        # Persist to DB
        create_posts(db, data)
        
        # Calculate summary
        total_posts = len(data)
        total_reach = sum(p['reach'] for p in data)
        total_impressions = sum(p['impressions'] for p in data)
        total_views = sum(p['views'] for p in data)
        
        return AnalysisSummary(
            total_posts=total_posts,
            total_reach=total_reach,
            total_impressions=total_impressions,
            total_views=total_views,
            status="success"
        )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
