# Используем базовый образ с Python 3.8
FROM python:3.9-slim

# Устанавливаем зависимости для работы с Python и телеграм ботом
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    wget \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*


# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Копируем и устанавливаем зависимости из requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Запуск приложения
CMD ["python", "main.py"]
