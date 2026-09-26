from sqlalchemy.orm import Session
from app.models.post import Post
from typing import List, Dict, Any
from datetime import datetime, date

def calculate_engagement(post: Post) -> int:
    return post.likes + post.comments + post.shares + post.saves

def calculate_engagement_rate(post: Post) -> float:
    engagements = calculate_engagement(post)
    if post.reach == 0:
        return 0.0
    return (engagements / post.reach) * 100

def get_overall_summary(db: Session) -> Dict[str, Any]:
    posts = db.query(Post).all()
    if not posts:
        return {
            "total_posts": 0,
            "total_reach": 0,
            "total_impressions": 0,
            "total_views": 0,
            "total_likes": 0,
            "total_comments": 0,
            "total_shares": 0,
            "total_saves": 0,
            "average_engagement_rate": 0.0
        }

    total_reach = sum(p.reach for p in posts)
    total_impressions = sum(p.impressions for p in posts)
    total_views = sum(p.views for p in posts)
    total_likes = sum(p.likes for p in posts)
    total_comments = sum(p.comments for p in posts)
    total_shares = sum(p.shares for p in posts)
    total_saves = sum(p.saves for p in posts)
    
    avg_engagement_rate = sum(calculate_engagement_rate(p) for p in posts) / len(posts)

    return {
        "total_posts": len(posts),
        "total_reach": total_reach,
        "total_impressions": total_impressions,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "total_shares": total_shares,
        "total_saves": total_saves,
        "average_engagement_rate": round(avg_engagement_rate, 2)
    }

def get_top_posts(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
    posts = db.query(Post).all()
    # Sort by reach (as primary indicator of performance for Month 1)
    sorted_posts = sorted(posts, key=lambda x: x.reach, reverse=True)
    
    return [
        {
            "post_id": p.instagram_post_id,
            "caption": p.caption[:50] + "..." if p.caption else "",
            "reach": p.reach,
            "engagement_rate": round(calculate_engagement_rate(p), 2),
            "post_type": p.post_type
        }
        for p in sorted_posts[:limit]
    ]

def get_performance_by_format(db: Session) -> List[Dict[str, Any]]:
    posts = db.query(Post).all()
    formats = {}
    
    for p in posts:
        if p.post_type not in formats:
            formats[p.post_type] = {"count": 0, "total_reach": 0, "total_engagement": 0}
        
        formats[p.post_type]["count"] += 1
        formats[p.post_type]["total_reach"] += p.reach
        formats[p.post_type]["total_engagement"] += calculate_engagement(p)

    result = []
    for fmt, data in formats.items():
        avg_reach = data["total_reach"] / data["count"] if data["count"] > 0 else 0
        avg_engagement = data["total_engagement"] / data["count"] if data["count"] > 0 else 0
        result.append({
            "format": fmt,
            "count": data["count"],
            "avg_reach": round(avg_reach, 2),
            "avg_engagement": round(avg_engagement, 2)
        })
    
    return result

def get_timeline_analytics(db: Session) -> List[Dict[str, Any]]:
    posts = db.query(Post).all()
    # Group by date
    timeline = {}
    for p in posts:
        day = p.posted_at.date() if isinstance(p.posted_at, datetime) else p.posted_at
        if day not in timeline:
            timeline[day] = {"reach": 0, "engagements": 0, "count": 0}
        
        timeline[day]["reach"] += p.reach
        timeline[day]["engagements"] += calculate_engagement(p)
        timeline[day]["count"] += 1

    sorted_days = sorted(timeline.keys())
    return [
        {
            "date": day.isoformat(),
            "reach": timeline[day]["reach"],
            "engagements": timeline[day]["engagements"],
            "post_count": timeline[day]["count"]
        }
        for day in sorted_days
    ]
