import pandas as pd
from typing import List, Dict, Any
from fastapi import HTTPException

# Schema A: Post-level export (Detailed)
POST_LEVEL_COLUMNS = [
    "post_id", "posted_at", "caption", "post_type", "reach", 
    "impressions", "likes", "comments", "shares", "saves", "views"
]

# Schema B: Timeline-level export (Aggregated)
TIMELINE_LEVEL_COLUMNS = ["Date", "Content interactions", "Viewers", "Views"]

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

    # DETECT SCHEMA
    is_post_level = all(col in df.columns for col in POST_LEVEL_COLUMNS)
    is_timeline_level = all(col in df.columns for col in TIMELINE_LEVEL_COLUMNS)

    if is_post_level:
        return _handle_post_level(df)
    elif is_timeline_level:
        return _handle_timeline_level(df)
    else:
        raise HTTPException(
            status_code=400, 
            detail="Unsupported CSV format. Please upload either a Post-level export or a Timeline-level export."
        )

def _handle_post_level(df: pd.DataFrame) -> List[Dict[str, Any]]:
    df = df[POST_LEVEL_COLUMNS].copy()
    numeric_cols = ["reach", "impressions", "likes", "comments", "shares", "saves", "views"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        if (df[col] < 0).any():
            raise HTTPException(status_code=400, detail=f"Column {col} contains negative values")
    
    df['posted_at'] = pd.to_datetime(df['posted_at'], errors='coerce')
    df = df.dropna(subset=['posted_at'])
    df['post_type'] = df['post_type'].apply(normalize_post_type)
    
    return df.to_dict(orient='records')

def _handle_timeline_level(df: pd.DataFrame) -> List[Dict[str, Any]]:
    # Map Timeline data to Post model
    # Date -> posted_at
    # Viewers -> reach
    # Content interactions -> likes (as a proxy for total engagement)
    # Views -> views
    
    processed_data = []
    for _, row in df.iterrows():
        try:
            date_val = pd.to_datetime(row['Date'])
            processed_data.append({
                "post_id": f"timeline_{date_val.strftime('%Y%m%d')}",
                "posted_at": date_val,
                "caption": f"Daily Summary for {date_val.strftime('%Y-%m-%d')}",
                "post_type": "OTHER",
                "reach": int(row['Viewers']) if pd.notnull(row['Viewers']) else 0,
                "impressions": int(row['Views']) if pd.notnull(row['Views']) else 0,
                "likes": int(row['Content interactions']) if pd.notnull(row['Content interactions']) else 0,
                "comments": 0,
                "shares": 0,
                "saves": 0,
                "views": int(row['Views']) if pd.notnull(row['Views']) else 0
            })
        except Exception:
            continue # Skip rows with corrupted dates
            
    if not processed_data:
        raise HTTPException(status_code=400, detail="No valid timeline data found in CSV")
        
    return processed_data
