
from fastapi import FastAPI
from pydantic import BaseModel
from shared.sqs_client import send_message
import os

app = FastAPI()

class UserRequest(BaseModel):
    text: str

QUEUE_URL = os.getenv("REQUEST_QUEUE_URL")

@app.post("/request/submit")
def submit_request(user_request: UserRequest):
    send_message(QUEUE_URL, user_request.text)
    return {"status": "submitted"}
