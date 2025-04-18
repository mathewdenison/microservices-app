
from fastapi import FastAPI
from pydantic import BaseModel
from shared.sqs_client import send_message
import os
from fastapi import Request


app = FastAPI()

class UserRequest(BaseModel):
    text: str

QUEUE_URL = os.getenv("REQUEST_QUEUE_URL")

@app.post("/submit")
def submit_request(user_request: UserRequest):
    send_message(QUEUE_URL, user_request.text)
    return {"status": "submitted"}

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def catch_all(full_path: str, request: Request):
    return {"path": full_path, "method": request.method}