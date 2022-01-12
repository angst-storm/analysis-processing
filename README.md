### Демо

Весь функционал доступен по
адресу [https://analysis-processing.herokuapp.com/](https://analysis-processing.herokuapp.com/).

### Документация сервиса

Документация кода на OpenAPI (Swagger) находится по
адресу [https://app.swaggerhub.com/apis-docs/Helloeverybody/AnalysisProcessing/v1](https://app.swaggerhub.com/apis-docs/Helloeverybody/AnalysisProcessing/v1)

## Установка ПО, необходимого для работы парсера

#### Tesseract

1. Скачать установщик [здесь](https://github.com/UB-Mannheim/tesseract/wiki)
2. Установить в папку `analysis-processing\restapi\parsers\tesseract`

#### Poppler

1. Скачать архив по [ссылке](https://drive.google.com/u/0/uc?id=1WU8SBkhBv_wx-dcNvztpaONI3_N29Cnj&export=download)
2. Распаковать в папку `analysis-processing\restapi\parsers`

## Инструкция по запуску API на локальном хосте

1. Открыть проект
2. Назначить или сгенерировать виртуальную область Python, установить зависимости из `requirements.txt`.
3. В папку `analysis-processing` положить файл с виртуальными переменными `.env` _(доступен только разработчикам)_.

### Команды для терминала Python:

1. `cd restapi` _(переход в папку restapi)_
2. `python manage.py migrate` _(создается база данных и внутри ее генерируются необходимые таблицы)_
3. `python manage.py collectstatic` _(собирает все статические файлы в одну папку)_
4. `python manage.py createsuperuser` _(запускается процесс регистрации пользователя, в следующих полях введите ник,
   почту и пароль)_
5. `python manage.py runserver` _(запуск сервера)_

### Взаимодействие с API:

#### Административная панель

- Переход по [localhost:8000/admin/](http://localhost:8000/admin/)

#### Получение результатов парсинга в ответе (возможна задержка)

- Метод GET (Адрес: [localhost:8000](http://localhost:8000/)) или переход по [localhost:8000](http://localhost:8000/):
  Форма с полем для отправки PDF
- Метод POST (Поля: {client_file: файл}; Адрес: [localhost:8000](http://localhost:8000/)) или отправка формы: Результат
  парсинга отправленного PDF

#### Получение результатов парсинга по id

- Метод GET ([localhost:8000/blood-tests/](http://localhost:8000/blood-tests/)) или переход по адресу вернет список PDF
  файлов, результат парсинга которых сохранен в базу данных
- Метод POST (Поля: {client_file: файл},
  Адрес: [http://localhost:8000/blood-tests/](http://localhost:8000/blood-tests/)) вернет ID результатов парсинга
  отправленного PDF
- Метод GET ([http://localhost:8000/blood-tests/id/](http://localhost:8000/blood-tests/id/)) или переход по адресу
  вернет результат парсинга PDF файла (хранящийся по ID)


### Виджеты

Код для вставки виджета на страницу:

```html

<div id="unique-id"></div>
<script src="https://analysis-processing.herokuapp.com/static/widget.js" type="text/javascript"></script>
<script type="text/javascript">
    widgetManager.init("unique-id");
</script>
```

При желании, `unique-id` можно заменить на любой другой уникальный id _(заменить необходимо в обоих местах)_.

Для взаимодействия с результатом работы API в объекте widgetManager предусмотрен метод actionWithResult(res),
принимающий на вход десериализованный объект ответа. Достаточно переопределить этот метод объекта _(по умолчанию метод
выводит всплывающее окно alert с результатом парсинга)_.

### Тесты

`python manage.py test` _(запуск тестов для моделей хранения данных и представления API)_

## Как запустить контейнер Docker

1. Установить [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
2. Ввести команду `docker-compose -f docker-compose.yml up -d`