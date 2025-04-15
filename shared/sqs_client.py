
import boto3
import os

sqs = boto3.client('sqs', region_name=os.getenv('AWS_REGION', 'us-east-2'))

def send_message(queue_url, message_body):
    response = sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
    return response

def receive_message(queue_url):
    messages = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    return messages.get('Messages', [])
