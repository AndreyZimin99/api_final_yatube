## API YATUBE:
В данном проекте я реализвал работу с постами, комментариями и подписками.

## Описание:

API для Yatube позволяет создавать посты, комментировать, изменять их и удалять и дает возможность подписаться на понравившихся авторов.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/AndreyZimin99/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
## Примеры запросов к  API:

### создание поста:

POST-запрос:

```
http://127.0.0.1:8000/api/v1/posts/
```

Данные запроса:

```
{
    "text": "Пост зарегистрированного пользователя."
}
```

### получить список комментариев:

GET-запрос:

```
http://127.0.0.1:8000/api/v1/posts/{{postid}}/comments/
```
