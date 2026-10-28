# Dockerfile для системы учёта заявок
FROM python:3.11-slim

# Рабочая папка
WORKDIR /app

# Сначала зависимости — для кэша слоёв
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Потом код
COPY app/ ./app/

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Команда запуска
CMD ["python", "-m", "app"]
