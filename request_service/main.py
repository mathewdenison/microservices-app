
from fastapi import FastAPI
from pydantic import BaseModel
from shared.sqs_client import send_message
import os
from fastapi import Request
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

class UserRequest(BaseModel):
    text: str

QUEUE_URL = os.getenv("REQUEST_QUEUE_URL")

@app.post("/submit")
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
    return {"path": full_path, "method": request.method}