# Бот в телеграмм с расписанием для КубГТУ

## ***Описание***
Бот в телеграм позваоляет просматривать расписание для группы 21-МБ-КТ1 вуза КубГТУ. (Можно изменить направление см. "Запуск")

## ***Технологии***
```
Python 3.8.5
Aiogram 2.22.1
SQLAlchemy 1.4.41
APScheduler 3.9.1
BeautifulSoup 4.11.1
Requests 2.28.1
ujson 5.4.0
```

## ***Запуск***
Запустите докер контейнер
```
docker-compose up
```
На этом всё!

### Если необходимо изменить группу
* В папке settings, в файле settings.json измените url на необходимый со страницы общедоступного расписания
* В корне проекта создайте файл .env и запишите в него данные
```
TG_API_TOKEN=токен_бота
TG_ADMIN_ID=ID_администратора_в_телеграме
DB_NAME=наименование_базы_данных
POSTGRES_USER=имя_пользователя_базы_данных
POSTGRES_PASSWORD=пароль_пользователя_бд
DB_HOST=адрес_бд
DB_PORT=порт_для_обращения_к_бд
```
* Измените docker-compose.yaml на
```
version: '3.7'

services:
  db:
    image: postgres:12.4
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    expose:
      - "5432"
    env_file:
      - .env
  web:
    build: .
    restart: always
    depends_on:
      - db
    env_file:
      - .env

volumes:
  postgres_data:
```
* Запустите docker
```
docker-compose up --build
```
