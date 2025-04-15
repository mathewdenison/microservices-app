import os
import openai
import time
import threading
from fastapi import FastAPI
import uvicorn
from shared.sqs_client import receive_message, send_message
import boto3

app = FastAPI()

REQUEST_QUEUE_URL = os.getenv("REQUEST_QUEUE_URL")
RESPONSE_QUEUE_URL = os.getenv("RESPONSE_QUEUE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'us-east-2'))

def ai_process(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that fixes grammar."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

def sqs_worker():
    while True:
        messages = receive_message(REQUEST_QUEUE_URL)
        for msg in messages:
            processed = ai_process(msg['Body'])
            send_message(RESPONSE_QUEUE_URL, processed)
            sqs.delete_message(QueueUrl=REQUEST_QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])
        time.sleep(2)

@app.on_event("startup")
def start_background_worker():
    thread = threading.Thread(target=sqs_worker)
    thread.daemon = True
    thread.start()

@app.get("/")
def health_check():
    return {"status": "AI Processor is running"}


