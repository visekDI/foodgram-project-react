#Foodrgam
Продуктовый помощник - дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект реализован на Django и DjangoRestFramework. Доступ к данным реализован через API-интерфейс. Документация к API написана с использованием Redoc.

Проект завернут в Docker-контейнеры;
Образы foodgram_frontend и foodgram_backend запушены на DockerHub;
Реализован workflow c автодеплоем на удаленный сервер и отправкой сообщения в Telegram;
Проект был развернут на сервере: https://visekzheldor.ddns.net/recipes
Админка проекта https://visekzheldor.ddns.net/recipes/admin/

Импорт CSV файлов осуществляется через панель админку
Заходиv в раздел Ингредиенты
Кликаем на Импорт
Выбираем CSV файл
Кликаем на загрузку

Установите на сервере docker и docker-compose.
Создайте файл .env. Шаблон для заполнения файла нахоится в /infra/.env.example.
Выполните команду docker-compose up -d --buld.
Выполните миграции docker-compose exec backend python manage.py migrate.
Создайте суперюзера docker-compose exec backend python manage.py createsuperuser.
Соберите статику docker-compose exec backend python manage.py collectstatic --no-input.
Для корректного создания рецепта через фронт, надо создать пару тегов в базе через админку.
Документация к API находится по адресу: http://localhost/api/docs/redoc.html.
Заполните базу ингредиентами через администрациооную пнель <http://localhost/admin


## 🛠 Стек технологий
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)



***
## Автор
-Василий Слободчиков @visekDI
