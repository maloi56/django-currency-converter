# Тестовое задание

Данный проект представляет собой веб-приложение, разработанное на базе фреймворка Django с использованием базы данных PostgreSQL, кэширования данных в Redis и планировщика Celery. Проект предоставляет пользователю возможность конвертировать валюту и получать актуальные курсы валют в российских рублях. Приложение также поддерживает авторизацию пользователей с использованием токенов.
<h3>Основной функционал</h3>

<h4>Конвертация валюты</h4>

Для конвертации валюты необходимо выполнить GET-запрос по следующему URL-адресу:
```
/api/convert?from=<код_валюты_1>&to=<код_валюты_2>&amount=<количество_валюты>
```
Параметры запроса:

* from (str): код валюты, из которой будет произведена конвертация (например, "USD" для долларов США).
* to (str): код валюты, в которую будет произведена конвертация (например, "EUR" для евро).
* amount (float): количество валюты, которое нужно конвертировать.

<h4>Получение текущих курсов валют</h4>

Для получения актуальных курсов валют в российских рублях необходимо выполнить GET-запрос по следующему URL-адресу:
```
/api/currency?valute=<код_валюты_опционально>
```
Параметр запроса (опционально):
* valute (str): Код валюты, для которой вы хотите получить курс (например, "USD" для долларов США). Если этот параметр не указан, будут возвращены курсы всех доступных валют.

<h3>Регистрация и авторизация</h3>

Для доступа к функциональности приложения необходима авторизация с использованием токенов.
Чтобы зарегистрироваться, выполните POST-запрос по следующему URL-адресу:
```
/users/
```
Необходимо указать следующие параметры в body запроса:

* username (str): имя пользователя.
* password (str): пароль пользователя.
* email (str): адрес электронной почты.

Чтобы получить токен для авторизации, выполните POST-запрос по следующему URL-адресу:
```
/auth/token/login/
```
Необходимо указать следующие параметры в теле запроса:

* username (str): имя пользователя.
* password (str): пароль пользователя.

Для доступа к методам приложения, необходимо включить заголовок "Authorization" со значением "Token" + 'token' в каждом запросе.

<h3>Технологический стек</h3>
Проект реализован с использованием следующих технологий:

* фреймворк Django для создания веб-приложения.
* система управления базами данных PostgreSQL для хранения пользовательских данных.
* сервер кэширования Redis для хранения актуальных курсов валют.
* планировщик задач Celery для автоматического обновления курсов валют каждые 12 часов.

Для обеспечения надежности приложения написаны основные тесты, включающие в себя проверки авторизации и корректной работы методов для конвертации валют и получения курсов валют.

Для удобства использования API доступны два вида документации:

* Redoc: Документация в формате ReDoc доступна по адресу /redoc.
* Swagger: Документация в формате Swagger доступна по адресу /swagger.
  
<h3> Инструкция по сборке проекта:</h3>

#### Build docker

```
sudo docker-compose build
```

#### Start docker

```
sudo docker-compose up
```

#### Build and run in detached mode

```
sudo docker-compose up --build -d
```

#### Stop docker-compose

```
sudo docker-compose down
```
#### Добавьте .env файл в папку src 

```
DEBUG=False
SECRET_KEY=<SECRET_KEY>

REDIS_HOST=redis
REDIS_PORT=6379

POSTGRES_DB=<DB_NAME>
POSTGRES_USER=<DB_USER>
POSTGRES_PASSWORD=<DB_PASS>
POSTGRES_HOST=db
POSTGRES_PORT=5432

DB_HOST=db
DB_NAME=<DB_NAME>
DB_USER=<DB_USER>
DB_PASS=<DB_PASS>

```
