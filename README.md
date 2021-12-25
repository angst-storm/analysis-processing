## Установка ПО, необходимого для работы парсера

- Tesseract:
    - Скачать установщик [здесь](https://github.com/UB-Mannheim/tesseract/wiki)
    - Установить в папку analysis-processing\restapi\parsers\tesseract

## Инструкция по запуску API на локальном хосте

Открыть проект, назначить или сгенерировать виртуальную область Python, установить зависимости из `requirements.txt`. В
папку analysis-processing положить секретный файл с виртуальными переменными `.env` (доступен только разработчикам).

### Далее команды для терминала Python:

- `cd restapi` (переход в папку restapi)
- `python manage.py migrate` (создается база данных и внутри ее генерируются необходимые таблицы)
- `python manage.py createsuperuser` (запускается процесс регистрации пользователя, в следующих поля введите ник, почту
  и пароль (два раза))
- `python manage.py runserver` (запуск сервера)

### Взаимодействие с API:

- Административная панель: переход по [localhost:8000/admin/](http://localhost:8000/admin/):
- Получение результатов парсинга в ответе (возможна задержка):
    - Метод GET (Адрес: [localhost:8000](http://localhost:8000/)) или переход
      по [localhost:8000](http://localhost:8000/): Форма с полем для отправки PDF
    - Метод POST (Поля: {pdf_file: файл}; Адрес: [localhost:8000](http://localhost:8000/)) или отправка формы: Результат
      парсинга отправленного PDF
- Получение результатов парсинга по id (id результатов возвращается мнгновенно, поле модели parsing_completed станет
  True после завершения парсинга)
    - Метод GET (Адрес: [localhost:8000/blood-tests/](http://localhost:8000/blood-tests/)) или переход
      по [localhost:8000/blood-tests/](http://localhost:8000/blood-tests/): Список PDF файлов, результат парсинга
      которых сохранен в базу данных
    - Метод POST (Поля: {pdf_file: файл}; Адрес: [localhost:8000/blood-tests/](http://localhost:8000/blood-tests/)): ID
      результатов парсинга отправленного PDF
    - Метод GET (Адрес: [localhost:8000/blood-tests/id/](http://localhost:8000/blood-tests/id/)) или переход
      по [localhost:8000/blood-tests/id/](http://localhost:8000/blood-tests/id/): Результат парсинга PDF файла (
      хранящийся по ID)

Также те же возможности доступны в открытом доступе по
адресу [https://analysis-processing.herokuapp.com/](https://analysis-processing.herokuapp.com/).

### Виджеты

Код для вставки виджета на страницу:

```html
<div id="unique-id"></div>
<script src="https://analysis-processing.herokuapp.com/static/widget.js" type="text/javascript"></script>
<script type="text/javascript">
    widgetManager.init("unique-id");
</script>
```

При желании, "unique-id" можно заменить на любой другой уникальный id (заменить необходимо в двух местах). 

Для взаимодействия с результатом работы API в объекте widgetManager предусмотрен метод actionWithResult(res), принимающий на
вход десериализованный объект ответа. Достаточно переопределить этот метод объекта (по умолчанию метод выводит
всплывающее окно alert с результатом парсинга).

## Как запустить контейнер Docker

- Установить Docker Desktop [тут](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- Ввести команду `docker-compose -f docker-compose.yml up -d`
- Приложение будет работать точно так же, как и при запуске через инструкцию выше
- При запуске контейнера Debug меняется на False, иметь ввиду
