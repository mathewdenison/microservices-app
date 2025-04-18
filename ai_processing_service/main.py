import os
import openai
import time
import threading
from fastapi import FastAPI
import uvicorn
from shared.sqs_client import receive_message, send_message
import boto3
import logging

logging.basicConfig(level=logging.INFO)

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
        try:
            messages = receive_message(REQUEST_QUEUE_URL)
            if messages:
                logging.info(f"Received {len(messages)} message(s) from request queue.")
            for msg in messages:
                logging.info(f"Processing message: {msg['Body']}")
                processed = ai_process(msg['Body'])
                send_message(RESPONSE_QUEUE_URL, processed)
                logging.info(f"Sent processed message to response queue.")
                sqs.delete_message(QueueUrl=REQUEST_QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])
        except Exception as e:
            logging.error(f"Error in SQS worker: {e}")
        time.sleep(2)

@app.on_event("startup")
def start_background_worker():
    thread = threading.Thread(target=sqs_worker)
    thread.daemon = True
    thread.start()

@app.get("/")
def health_check():
    return {"status": "AI Processor is running"}


