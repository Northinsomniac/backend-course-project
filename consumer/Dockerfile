
FROM python:3.12.4-slim as builder

WORKDIR /app


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


FROM python:3.12.4-slim

WORKDIR /app


COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app


ENV PYTHONPATH /app


CMD ["python", "consumer/rabbitmq_consumer.py"]

