from fastapi import APIRouter
from sentinel_x.modules.iot.service import iot_service

router = APIRouter()

@router.get("/devices")
async def get_all_devices():
    """Get the status and location of all connected IoT sensors/devices."""
    return iot_service.get_all_devices()

@router.post("/ingest/{device_id}")
async def post_sensor_data(device_id: str, reading: float):
    """Ingest live telemetry from a connected field device."""
    return iot_service.ingest_sensor_data(device_id, reading)
