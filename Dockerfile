# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY ./requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Копируем исходный код
COPY ./app /app/app
COPY ./tests /app/tests

# Устанавливаем переменную окружения для удобства
ENV PYTHONPATH=/app

# Открываем порт
EXPOSE 8000

# Определяем команду по умолчанию для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
