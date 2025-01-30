# FROM python:3.12.4

# WORKDIR /app


# COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# ENV PYTHONPATH /app

# CMD ["/usr/local/bin/python", "consumer.py"]
    
# Используем многоэтапную сборку для уменьшения размера итогового образа
FROM python:3.12.4-slim as builder

WORKDIR /app

# Копируем только requirements.txt для кэширования слоя с зависимостями
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY . .

# Финальный образ
FROM python:3.12.4-slim

WORKDIR /app

# Копируем зависимости из builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app

# Устанавливаем переменную окружения PYTHONPATH
ENV PYTHONPATH /app

# Указываем команду для запуска потребителя
CMD ["python", "consumer/rabbitmq_consumer.py"]

