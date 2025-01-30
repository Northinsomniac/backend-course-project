# API (доисторической) соцсети для курса Backend-python

## Инструкция по запуску
```bash
git clone https://github.com/Northinsomniac/backend-course-project.git
cd backend-course-project
docker-compose -f docker-compose.yml -p my_backend up --build
```

docker-compose.overrite.yml для облегченной версии (запуск тестов или только апи + бд)

### .env файл - структура
для тестов был создан github secret с env переменными, при клонировании репозитория потребуется создать свой .env в корне проекта.

Его структура:
```yml
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=

DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_NAME=
DATABASE_HOSTNAME=
DATABASE_PORT=5432

RABBITMQ_USER=
RABBITMQ_PASSWORD=
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
```

## Метрики 

Сбор метрик метрик осуществляется с помощью Prometheus, визуализирует Graphana

(тут небольшой ускоренный видос) 

[Демонстрация](https://drive.google.com/drive/folders/1am_US8lFRs1ZaNnND1MmaoHYuFWD4N46)

