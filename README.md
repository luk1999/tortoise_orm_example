# Tortoise ORM example app

## Prerequisites
Make sure that you have Python 3.7 or later installed.

You can use pipenv.

Go to project directory and run command (you can replace `3.7` by Python version you've installed).
```bash
pipenv --python 3.7
pipenv install
```

## Database configuration
If you don't have MySQL then you can use dockerized version:
```bash
docker run -p 3306:3306 --name tortoise-example-mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:8.0
docker start tortoise-example-mysql
```

Get your container id (`docker ps`) and connect to container:
```bash
docker exec -it [container_id] mysql -uroot -proot
```

Run following queries to create user and databases:
```sql
CREATE DATABASE IF NOT EXISTS tortoise;
CREATE DATABASE IF NOT EXISTS alchemy;
CREATE USER 'test_user'@'%' IDENTIFIED BY 'test1234';
GRANT ALL PRIVILEGES ON tortoise.* TO 'test_user'@'%';
GRANT ALL PRIVILEGES ON alchemy.* TO 'test_user'@'%';
```

## First run
Go to project directory and activate venv:
```bash
pipenv shell
```

Go to `src_tortoise` directory.

Run migrations:
```bash
aeris upgrade
```

Install fixture:
```bash
python app.py init
```

## Run app
### Tortoise ORM version
Activate venv in project directory:
```bash
pipenv shell
```

Go to `src_tortoise` directory.

Run server:
```bash
python app.py
```

Open `http://localhost:8080/user` in your web browser.

## Endpoints list
 - GET `/user` - list of users with `username` and `email`
 - GET `/user/name` - list of usernames
 - GET `/user/full` - list of users with assigned groups and addresses
