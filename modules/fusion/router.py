from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from sentinel_x.modules.fusion.service import fusion_service
import shutil
import os
import json

router = APIRouter()

@router.post("/ingest")
async def ingest_intelligence(
    image: UploadFile = File(None),
    audio: UploadFile = File(None),
    location: str = Form(None) # JSON string of location
):
    """
    Unified endpoint for multimodal intelligence ingestion.
    """
    loc_data = json.loads(location) if location else None
    image_bytes = await image.read() if image else None
    
    audio_path = None
    if audio:
        audio_path = f"temp_audio_{audio.filename}"
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)
    
    try:
        report = await fusion_service.process_intelligence(
            image_bytes=image_bytes,
            audio_path=audio_path,
            location=loc_data
        )
        return {"status": "success", "report_id": str(report.get("_id", "pending")), "report": report}
    finally:
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)

@router.get("/reports")
async def get_reports(limit: int = 10):
    from sentinel_x.db.mongodb import get_database
    db = get_database()
    reports = await db.intelligence.find().sort("timestamp", -1).to_list(limit)
    for r in reports:
        r["_id"] = str(r["_id"])
    return reports

@router.post("/train")
async def trigger_learning():
    """
    Trigger a continuous learning cycle using captured data.
    """
    from sentinel_x.modules.fusion.anomaly import anomaly_detector
    await anomaly_detector.continuous_learning()
    return {"status": "Continuous learning cycle triggered", "model": "IsolationForest"}
