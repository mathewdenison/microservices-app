
FROM python:3.11-slim
WORKDIR /app
COPY shared ./shared
COPY request_servicemain.py .
RUN pip install fastapi uvicorn boto3
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
