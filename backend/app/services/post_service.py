from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.analytics import PostCreate
from typing import List

def create_posts(db: Session, posts_data: List[dict]):
    created_posts = []
    for data in posts_data:
        # Use instagram_post_id as the unique identifier to avoid duplicates
        # In a real app, we might use upsert, but for MVP, we'll check for existence
        existing = db.query(Post).filter(Post.instagram_post_id == str(data['post_id'])).first()
        if not existing:
            post = Post(
                instagram_post_id=str(data['post_id']),
                posted_at=data['posted_at'],
                caption=data.get('caption', ""),
                post_type=data['post_type'],
                reach=data['reach'],
                impressions=data['impressions'],
                likes=data['likes'],
                comments=data['comments'],
                shares=data['shares'],
                saves=data['saves'],
                views=data['views']
            )
            db.add(post)
            created_posts.append(post)
    
    db.commit()
    return created_posts
