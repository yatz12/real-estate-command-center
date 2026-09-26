from sqlalchemy import Column, Integer, String, DateTime, Float
from app.db.database import Base
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    instagram_post_id = Column(String, unique=True, index=True)
    posted_at = Column(DateTime)
    caption = Column(String)
    post_type = Column(String)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
