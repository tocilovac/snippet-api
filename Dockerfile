FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:///./snippets.db
ENV REDIS_URL=redis://localhost:6379/0

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
