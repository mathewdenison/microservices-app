import time
import os
from shared.sqs_client import receive_message, send_message
import boto3

REQUEST_QUEUE_URL = os.getenv("REQUEST_QUEUE_URL")
RESPONSE_QUEUE_URL = os.getenv("RESPONSE_QUEUE_URL")

sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'us-east-1'))

def ai_process(text):
    return f"[AI Response] {text}"

def run():
    while True:
        messages = receive_message(REQUEST_QUEUE_URL)
        for msg in messages:
            processed = ai_process(msg['Body'])
            send_message(RESPONSE_QUEUE_URL, processed)
            sqs.delete_message(QueueUrl=REQUEST_QUEUE_URL, ReceiptHandle=msg['ReceiptHandle'])
        time.sleep(2)


if __name__ == "__main__":
    print("Starting AI processing service...")
    run()
