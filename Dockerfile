FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos "" appuser \
    && mkdir -p /app/instance \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["sh", "-c", "python -m scripts.init_db && flask --app run:app run --host=0.0.0.0 --port=5000 --no-debugger --no-reload"]
