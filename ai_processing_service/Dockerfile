
FROM python:3.11-slim
WORKDIR /app
COPY shared ./shared
COPY ai_processing_service/main.py .
RUN pip install boto3
CMD ["python", "main.py"]
