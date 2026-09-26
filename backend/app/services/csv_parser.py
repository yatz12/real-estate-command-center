import pandas as pd
from typing import List, Dict, Any
from app.schemas.analytics import PostCreate
from fastapi import HTTPException

REQUIRED_COLUMNS = [
    "post_id", "posted_at", "caption", "post_type", "reach", 
    "impressions", "likes", "comments", "shares", "saves", "views"
]

SUPPORTED_TYPES = {"REEL", "CAROUSEL", "IMAGE", "STORY", "OTHER"}

def normalize_post_type(pt: Any) -> str:
    if not isinstance(pt, str):
        return "OTHER"
    pt_upper = pt.upper().strip()
    return pt_upper if pt_upper in SUPPORTED_TYPES else "OTHER"

def parse_instagram_csv(file_path: str) -> List[Dict[str, Any]]:
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="CSV file is empty")

    # Check for required columns
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise HTTPException(
            status_code=400, 
            detail=f"Missing required columns: {', '.join(missing_cols)}"
        )

    # Basic data cleaning
    df = df[REQUIRED_COLUMNS].copy()
    
    # Ensure numeric columns are numeric, replace NaN with 0
    numeric_cols = ["reach", "impressions", "likes", "comments", "shares", "saves", "views"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        if (df[col] < 0).any():
            raise HTTPException(status_code=400, detail=f"Column {col} contains negative values")

    # Normalize dates
    df['posted_at'] = pd.to_datetime(df['posted_at'], errors='coerce')
    if df['posted_at'].isna().any():
        # We'll flag this or handle it; for MVP, we'll reject rows with invalid dates
        df = df.dropna(subset=['posted_at'])
        if df.empty:
            raise HTTPException(status_code=400, detail="No valid dates found in CSV")

    # Normalize post type
    df['post_type'] = df['post_type'].apply(normalize_post_type)

    return df.to_dict(orient='records')
