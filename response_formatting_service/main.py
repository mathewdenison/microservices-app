
import time
import os
from fastapi import FastAPI
from shared.sqs_client import receive_message
from threading import Thread

app = FastAPI()

RESPONSE_QUEUE_URL = os.getenv("RESPONSE_QUEUE_URL")
latest_response = None

def format_response(text):
    return {"formatted_response": text.upper()}

def background_worker():
    global latest_response
    while True:
        messages = receive_message(RESPONSE_QUEUE_URL)
        for msg in messages:
            formatted = format_response(msg['Body'])
            latest_response = formatted
            print("Formatted Response:", formatted)
        time.sleep(2)

@app.get("/responseFormattingService/latest")
def get_latest():
    if latest_response:
        return latest_response
    return {"formatted_response": None}

if __name__ == "__main__":
    Thread(target=background_worker, daemon=True).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
