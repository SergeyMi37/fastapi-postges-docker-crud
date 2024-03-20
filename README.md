# FastAPI demo with Postgres using SQLAlchemy

This is a simplest demo of FastAPI on Postgres using SQLAlchemy

## Using

Build docker compose environment

```shell
docker-compose build
```

Start in development mode

```shell
docker-compose up app
```

Access docs page: http://localhost:8000/docs


## Создание виртуального окружения для проекта
### Для Windows
```cmd
python -m venv env
source env/Scripts/activate
```

### Для Linux
```bash
python3 -m venv env
source env/bin/activate
```

# Как запустить бэкэнд локально

## Копировать в файл .env переменную окружения DATABASE_URL из файла env.sample

## Установить СУБД PostgreSql
создать базу данных testdemo программой pgAdmin
или из терминала
```bash
sudo -u postgres psql
postgres-# CREATE DATABASE testdemo;
postgres-# \conninfo
You are connected to database "postgres" as user "postgres" via socket in "/var/run/postgresql" at port "5432".
postgres-# \?
postgres-# alter user postgres with password 'postgres';
postgres-# \q
```

## Установки зависимости:  
```bash
pip install -r requirements.txt
```

## Создать .env файл на основе env.sample


## Запустить миграции
```bash
alembic upgrade head
```

## Необходимо перейти в каталог бэкенд:  
```bash
uvicorn app.main:app --workers 1 --host 0.0.0.0 --port 8000 --env-file .env
```
или
```
python -m uvicorn app.main:app --workers 1 --host 0.0.0.0 --port 8000 --env-file .env
```

## Создать в директории frontend/ файл .env на основе env.example
И прописать актуальные параметры доступа к эндпоинтам Swagger
Если нужно подключаться к эндпоинтам Swagger контейнера, то менять настройки не надо


## Загрузить образы и собрать контейнеры
 Если ошибка: services.flask.depends_on contains an invalid type, it should be an array? 
 то нужно обновить docker-compose до версии 1.29.2
 sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  
```
docker-compose build --no-cache
```

## Запустить контейнеры
```
docker-compose up -d
```
## Смотреть состояние контейнеров
```
docker-compose ps
```
## Смотреть протоколы
```
docker-compose logs
```
## Остановить контейнеры
```
docker-compose stop
```
## Убить контейнеры
```
docker-compose kill
```
### stoped and clean all containers
```
docker stop $(docker ps -a -q) &&  docker rm $(docker ps -a -q) && docker system prune -f
```
### rmi images
```
docker rmi $(docker images -a -q) && docker system prune -f
```


# Работа с репозиторием

## Клонировать ранее созданную ветку из репо
```
git clone https://git.lab.nexus/ctz/lab/rating/inspection.git -b msw-dockerize
```

## Основные команды сохранения изменений
```
git add *
git commit -am "комментарий"
git push
```
## Позволяет на время архивировать (или «отложить») изменения, сделанные в рабочей копии, чтобы вы могли применить их позже
```
git stash
git stash pop
git stash drop
```

## Получить последнюю версию из удаленного репозитория
```
git pull
```
