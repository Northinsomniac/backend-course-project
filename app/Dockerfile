# Используем легковесный Python-образ
FROM python:3.12.4-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта внутрь контейнера
COPY . .

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt ./ 
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменную PYTHONPATH для корректного импорта
ENV PYTHONPATH="/app"

# Открываем порт
EXPOSE 8080

# Запуск FastAPI-приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
