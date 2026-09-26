from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/summary")
async def get_summary():
    return {"message": "Analytics summary endpoint - placeholder"}
