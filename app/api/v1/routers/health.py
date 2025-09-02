from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(prefix="/v1", tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/ready")
def ready():
    return {"status": "ready"}