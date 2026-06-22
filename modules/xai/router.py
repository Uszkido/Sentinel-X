from fastapi import APIRouter, HTTPException
from sentinel_x.modules.xai.service import xai_service
from sentinel_x.db.mongodb import get_database
from bson import ObjectId

router = APIRouter()

@router.get("/explain/{report_id}")
async def explain_report(report_id: str):
    """
    Generate an explanation for a specific intelligence report.
    """
    db = get_database()
    report = await db.intelligence.find_one({"_id": ObjectId(report_id)})
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    explanation = xai_service.explain_intelligence(report)
    return {"report_id": report_id, "explanation": explanation}
