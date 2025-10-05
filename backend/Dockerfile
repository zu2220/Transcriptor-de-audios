FROM python:3.11-slim


# Instalar ffmpeg y dependencias del sistema
RUN apt-get update && apt-get install -y ffmpeg git build-essential libsndfile1 && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


COPY app /app


ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]