from fastapi import APIRouter
from sentinel_x.modules.vision.router import router as vision_router
from sentinel_x.modules.nlp.router import router as nlp_router
from sentinel_x.modules.fusion.router import router as fusion_router
from sentinel_x.modules.xai.router import router as xai_router
from sentinel_x.modules.federated.router import router as federated_router
from sentinel_x.modules.drone.router import router as drone_router
from sentinel_x.modules.iot.router import router as iot_router
from sentinel_x.api.v1.endpoints.auth import router as auth_router

api_router = APIRouter()

@api_router.get("/health")
async def health_check():
    return {"status": "ok", "message": "SENTINEL-X API is healthy"}

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(vision_router, prefix="/vision", tags=["vision"])
api_router.include_router(nlp_router, prefix="/nlp", tags=["nlp"])
api_router.include_router(fusion_router, prefix="/fusion", tags=["fusion"])
api_router.include_router(xai_router, prefix="/xai", tags=["xai"])
api_router.include_router(federated_router, prefix="/federated", tags=["federated"])
api_router.include_router(drone_router, prefix="/drone", tags=["drone"])
api_router.include_router(iot_router, prefix="/iot", tags=["iot"])
