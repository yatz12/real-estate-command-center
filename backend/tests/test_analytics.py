import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models.post import Post
from app.services.analytics_service import (
    calculate_engagement, 
    calculate_engagement_rate, 
    get_overall_summary
)

# Test Database Setup
TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

def test_calculate_engagement():
    post = Post(likes=10, comments=5, shares=2, saves=3)
    assert calculate_engagement(post) == 20

def test_calculate_engagement_rate_normal():
    post = Post(reach=1000, likes=10, comments=5, shares=2, saves=3)
    assert calculate_engagement_rate(post) == 2.0 # (20/1000)*100

def test_calculate_engagement_rate_zero_reach():
    post = Post(reach=0, likes=10, comments=5, shares=2, saves=3)
    assert calculate_engagement_rate(post) == 0.0

def test_overall_summary_empty_db(db):
    summary = get_overall_summary(db)
    assert summary["total_posts"] == 0
    assert summary["average_engagement_rate"] == 0.0

def test_overall_summary_with_data(db):
    post1 = Post(instagram_post_id="1", reach=1000, likes=10, comments=0, shares=0, saves=0)
    post2 = Post(instagram_post_id="2", reach=2000, likes=20, comments=0, shares=0, saves=0)
    db.add_all([post1, post2])
    db.commit()
    
    summary = get_overall_summary(db)
    assert summary["total_posts"] == 2
    assert summary["total_reach"] == 3000
    # ER1 = (10/1000)*100 = 1%
    # ER2 = (20/2000)*100 = 1%
    # Avg = (1+1)/2 = 1%
    assert summary["average_engagement_rate"] == 1.0
