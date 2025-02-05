# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY requirements.txt ./
COPY config.py ./
COPY bot.py ./
ENV BOT_TOKEN=***

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем, какую команду выполнять при старте контейнера
CMD ["python", "bot.py"]
