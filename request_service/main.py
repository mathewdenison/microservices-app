import os
import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
from shared.sqs_client import send_message

# === Setup Logging to stdout ===
import sys
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# === Initialize App ===
app = FastAPI()

# === Data Model ===
class UserRequest(BaseModel):
    text: str

# === Get Environment Variables ===
QUEUE_URL = os.getenv("REQUEST_QUEUE_URL")

if not QUEUE_URL:
    logging.error("REQUEST_QUEUE_URL environment variable not set.")
else:
    logging.info(f"Using SQS queue URL: {QUEUE_URL}")

# === Routes ===

@app.post("/request/submit")
def submit_request(user_request: UserRequest):
    try:
        logging.info(f"Received text: {user_request.text}")
        send_message(QUEUE_URL, user_request.text)
        logging.info(f"Message sent to SQS queue: {QUEUE_URL}")
        return {"status": "submitted"}
    except Exception as e:
        logging.error(f"Failed to send message to SQS: {e}")
        return {"status": "error", "message": str(e)}

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(full_path: str, request: Request):
    body = await request.body()
    logging.warning(f"Unhandled path received: /{full_path} | Method: {request.method} | Body: {body.decode('utf-8')}")
    return {"path": full_path, "method": request.method}
