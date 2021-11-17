## Инструкция по запуску API на локальном хосте #

При первом открытии проекта в Pycharm и подключении к нему интерпретатора Python в проекте должна была сгенерироваться
папка venv (виртуальная область Python)

Также при первом открытии проекта Pycharm должен автоматически загрузить библиотеки, перечисленные в requirements.txt,
если этого не произошло, установите их при помощи Python Packages вручную

### Далее команды для терминала Python:

- `cd restapi` (переход в папку restapi)
- `python manage.py makemigrations` (при помощи файла-мененджера создаются миграции моделей данных для базы данных)
- `python manage.py migrate` (созданные миграции переносятся в базу данных)  
  *(команды выше необходимо вводить при каждом изменении моделей)*
- `python manage.py createsuperuser` (запускается процесс регистрации пользователя, в следующих поля введите ник, почту
  и пароль (два раза))
- `python manage.py runserver` (запуск сервера)

### Взаимодействие с API:  
- Административная панель: переход по [localhost:8000/admin/](http://localhost:8000/admin/):
- Получение результатов парсинга без сохранения в базу данных (возможна задержка): 
  - Метод GET (Адрес: [localhost:8000](http://localhost:8000/)) или переход по [localhost:8000](http://localhost:8000/): Форма с полем для отправки PDF
  - Метод POST (Поля: {pdf_file: файл}; Адрес: [localhost:8000](http://localhost:8000/)) или отправка формы: Результат парсинга отправленного PDF
- Получение результатов парсинга с сохранением в базу данных (id результатов возвращается мнгновенно, поле модели parsing_completed станет True после завершения парсинга)
  - Метод GET (Адрес: [localhost:8000/blood-tests/](http://localhost:8000/blood-tests/)) или переход по [localhost:8000/blood-tests/](http://localhost:8000/blood-tests/): Список PDF файлов, результат парсинга которых сохранен в базу данных
  - Метод POST (Поля: {pdf_file: файл}; Адрес: [localhost:8000/blood-tests/](http://localhost:8000/blood-tests/)): ID результатов парсинга отправленного PDF
  - Метод GET (Адрес: [localhost:8000/blood-tests/id/](http://localhost:8000/blood-tests/id/)) или переход по [localhost:8000/blood-tests/id/](http://localhost:8000/blood-tests/id/): Результат парсинга PDF файла (хранящийся по ID)

## Инструкция для подключения Tesseract OCR к проекту

Скачать установщик Tesseract [здесь](https://github.com/UB-Mannheim/tesseract/wiki) и установить в папку
analysis-processing\analysis_ocr\tesseract (при установке в `Additional language data` обязательно выбрать пункт `Russian` и при необходимости создать папку tesseract)

## Как запустить контейнер Docker

- Установить Docker Desktop [тут](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
- Ввести команду `docker-compose -f docker-compose.yml up -d`
- Приложение будет работать точно так же, как и при запуске через инструкцию выше
- При запуске контейнера Debug меняется на False, иметь ввиду