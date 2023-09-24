# Foodgram
«Продуктовый помощник». С помощью сервиса пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Установка проекта на сервере
Установить Докер:
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
sudo systemctl status docker
Установить и настроить nginx на свободный порт (см. nginx.default.example):
sudo apt install nginx -y
sudo systemctl start nginx
sudo nano /etc/nginx/sites-enabled/default
sudo nginx -t
sudo service nginx reload
Создать папку foodgram и скопировать в нее файл docker-compose.production.yml и папку data
В папке foodgram создать и заполнить файл с переменными окружен .env (см. env.example)
Запустить docker compose:
sudo docker compose -f docker-compose.production.yml up -d
Выполнить миграции, собрать статические файлы бэкенда и скопировать их в /backend_static/static/:
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
Загрузить данные в БД:
sudo docker compose -f docker-compose.production.yml exec backend python manage.py import_csv recipes/data/ingredients.csv
Создать адмнистратора для управления сайтом:
docker compose exec -it backend python manage.py createsuperuser


## исходники
foodgram_domain: https://visekzheldor.ddns.net/
dockerhub_username: visekdi
ip: 84.201.142.105
SUPERUSER: email:visekDI@yandex.ru,
           password: Wqpyt9Nx

## автор
Слободчиков Василий @visekDI
