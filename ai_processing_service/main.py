import os
import time
import threading
import logging
from fastapi import FastAPI
from openai import OpenAI
import boto3
from shared.sqs_client import receive_message, send_message

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Create FastAPI app
app = FastAPI()

# Environment variables
REQUEST_QUEUE_URL = os.getenv("REQUEST_QUEUE_URL")
RESPONSE_QUEUE_URL = os.getenv("RESPONSE_QUEUE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI v1 client
client = OpenAI(api_key=OPENAI_API_KEY)

# Boto3 SQS client
sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'us-east-2'))

def ai_process(text):
    logging.info(f"Calling OpenAI with text: {text}")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that fixes grammar."},
            {"role": "user", "content": text}
        ]
    )
    result = response.choices[0].message.content.strip()
    logging.info(f"OpenAI response: {result}")
    return result

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
                logging.info("Sending response to SQS complete.")
                sqs.delete_message(QueueUrl=REQUEST_QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])
        except Exception as e:
            logging.error(f"Error in SQS worker: {e}")
        time.sleep(2)

@app.on_event("startup")
def start_worker():
    thread = threading.Thread(target=sqs_worker)
    thread.daemon = True
    thread.start()

@app.get("/")
def health_check():
    return {"status": "AI Processor is running"}
