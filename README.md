# Test_backend_task

Ссылка на GitHub: https://github.com/Millitarian/Test_backend_task

Инструкция:

1. Клонировать репозиторий:
    git clone https://github.com/Millitarian/Test_backend_task


2. Установить зависимости:
    poetry install

3. Создать .env файл в корневой директории проекта:
   Содержимое .env:
       DATABASE_HOST = "localhost"
       DATABASE_PORT = "5432"
       DATABASE_USERNAME = "postgres"
       DATABASE_PASSWORD = "postgres"
       DATABESE_NAME = "backendTask"
       RABBITMQ_HOST = "localhost"
       RABBITMQ_PORT = "5672"
       RABBITMQ_USERNAME = "guest"
       RABBITMQ_PASSWORD = "guest"
       RADIS_HOST = "localhost"
       RADIS_PORT = "6379"


5. Запустить проект:
    uvicorn main:app

