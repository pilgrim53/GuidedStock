# Pmgstock

## Setup Project using Docker

Just make sure you have installed `docker` in your machine.

1. Clone the project from git repository and move into the project directory.

```sh

cd pmgstock/
```

2. Create a `.env` file in the project folder.

```sh
touch .env
```

3. Add the below content into `.env` file.

```txt
DEBUG=True
SECRET_KEY='_*ox4(kcm$dxvat)8z^als0r=b+ykpf&m1lhj4kfwpoxpt)5xz'
ALLOWED_HOSTS=127.0.0.1,PMG-ZENBOOK2
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=admin@example.com
EMAIL_HOST_PASSWORD=password
EMAIL_USE_TLS=True
```

4. Then run the following command to setup project using docker:

```sh 
docker-compose up -d --build
```

5. Migrate the database

```sh
docker-compose exec web python manage.py migrate
```

You can go to the http:///127.0.0.1 to view the application running.

### Create a Super User

Create a super user with following command; So you can login into the admin site:

```sh
docker-compose exec web python manage.py createsuperuser
```

### Setup Cronjob for updating the stock data

```sh
docker-compose exec web python manage.py cronjob
```