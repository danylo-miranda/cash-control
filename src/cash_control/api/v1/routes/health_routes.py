from fastapi import APIRouter

router = APIRouter(tags=["Healt"])

@router.get("/health")
def health_check():
    return {"status": "ok"}

