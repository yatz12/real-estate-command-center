from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class PostBase(BaseModel):
    instagram_post_id: str
    posted_at: datetime
    caption: Optional[str] = ""
    post_type: str
    reach: int = Field(ge=0)
    impressions: int = Field(ge=0)
    likes: int = Field(ge=0)
    comments: int = Field(ge=0)
    shares: int = Field(ge=0)
    saves: int = Field(ge=0)
    views: int = Field(ge=0)

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AnalysisSummary(BaseModel):
    total_posts: int
    total_reach: int
    total_impressions: int
    total_views: int
    status: str = "success"
