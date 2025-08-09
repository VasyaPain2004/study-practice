FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/instance

COPY note-management-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY note-management-app/ .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--workers", "1", "--preload"]