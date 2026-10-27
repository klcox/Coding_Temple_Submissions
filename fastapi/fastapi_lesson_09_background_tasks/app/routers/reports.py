from fastapi import APIRouter, BackgroundTasks, HTTPException
import time
import uuid


router = APIRouter()


report_store: dict[str, dict] = {}
notification_log: list[dict] = []


# ── Background task functions ─────────────────────────────────────────────────

def generate_report(report_id: str, report_type: str, rows: int) -> None:
    """Simulates a long-running report-generation task."""

    report_store[report_id]["status"] = "processing"     
    
    time.sleep(10)  # Simulates the time taken to complete the operation

    report_store[report_id].update({
        "status": "completed",        
        "result": {
            "report_type": report_type,
            "num_rows": rows
        }
    })    


def send_notification(recipient: str, message: str) -> None:
    """Simulates sending a notification (email/SMS) in the background."""

    time.sleep(10)

    notification_log.append({
        "status": "sent",
        "recipient": recipient,
        "message": message
    })    

# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.post("/")
def create_report(background_tasks: BackgroundTasks, report_type: str = "sales", rows: int = 100):
    """Kicks off report generation and returns immediately with a report_id."""

    report_id = str(uuid.uuid4())  # Generates Universally Unique Identifier

    report_store[report_id] = {"status": "pending"}

    background_tasks.add_task(generate_report, report_id, report_type, rows)

    return {"report_id": report_id, "status": "pending"}


@router.get("/{report_id}")
def get_report_status(report_id: str):
    """Returns the current status (and result if ready) of a report."""

    if report_id not in report_store:   
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found.")

    return report_store[report_id]


@router.post("/notifications")
def send_notification_endpoint(
    background_tasks: BackgroundTasks,
    recipient: str = "user@example.com",
    message: str = "Hello!",
):
    """Queues a notification to be sent in the background and returns immediately with a 'queued' status."""

    background_tasks.add_task(send_notification, recipient, message)

    return {"notification_status": "queued"}


@router.get("/notifications/log")
def get_notification_log():
    """Returns the notification log and its current contents."""
     
    return notification_log