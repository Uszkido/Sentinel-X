from fastapi import APIRouter, BackgroundTasks
from sentinel_x.modules.federated.service import federated_service

router = APIRouter()

@router.post("/start-training")
async def start_training(rounds: int = 3, background_tasks: BackgroundTasks = None):
    """
    Start a federated learning training round.
    """
    # Run server in background to avoid blocking API
    if background_tasks:
        background_tasks.add_task(federated_service.start_federated_server, rounds)
    return {"message": "Federated training session initiated.", "rounds": rounds}

@router.get("/status")
async def get_status():
    return {"status": "Operational", "active_clients": "..."}
