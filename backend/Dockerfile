FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-deu \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Allow configurable log level via LOG_LEVEL env (default info)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --log-level ${LOG_LEVEL:-info}"]
