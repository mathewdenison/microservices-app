FROM python:3.11-slim
WORKDIR /app

COPY shared ./shared
COPY ai_processing_service/main.py .

RUN pip install fastapi uvicorn boto3 openai>=1.0.0

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]