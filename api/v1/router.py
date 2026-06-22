from fastapi import APIRouter
from sentinel_x.modules.vision.router import router as vision_router
from sentinel_x.modules.nlp.router import router as nlp_router
from sentinel_x.modules.fusion.router import router as fusion_router
from sentinel_x.modules.xai.router import router as xai_router

api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    return {"status": "ok", "message": "SENTINEL-X API is healthy"}

api_router.include_router(vision_router, prefix="/vision", tags=["vision"])
api_router.include_router(nlp_router, prefix="/nlp", tags=["nlp"])
api_router.include_router(fusion_router, prefix="/fusion", tags=["fusion"])
api_router.include_router(xai_router, prefix="/xai", tags=["xai"])
