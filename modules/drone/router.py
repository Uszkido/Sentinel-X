from fastapi import APIRouter, HTTPException
from sentinel_x.modules.drone.service import drone_service
from pydantic import BaseModel

router = APIRouter()

class MissionRequest(BaseModel):
    drone_id: str
    lat: float
    lng: float
    alt: float = 300

@router.get("/telemetry")
async def get_telemetry():
    """Get real-time position and status of all drones."""
    return drone_service.get_telemetry()

@router.post("/dispatch")
async def dispatch_mission(mission: MissionRequest):
    """Manually dispatch a drone to a coordinate."""
    result = drone_service.dispatch_drone(mission.drone_id, mission.lat, mission.lng, mission.alt)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@router.post("/autonomous")
async def trigger_autonomous_response(lat: float, lng: float):
    """Trigger the nearest drone to investigate an anomaly."""
    return drone_service.autonomous_dispatch(lat, lng)

@router.post("/swarm")
async def trigger_swarm_mission(formation: str, lat: float, lng: float):
    """Execute a coordinated swarm mission (CIRCLE, GRID)."""
    return drone_service.execute_swarm_mission(formation, lat, lng)
