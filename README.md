# Инструкция по запуску API на локальном хосте #

При первом открытии проекта в Pycharm и подключении к нему интерпретатора Python в проекте должна была сгенерироваться
папка venv (виртуальная область Python)

Также при первом открытии проекта Pycharm должен автоматически загрузить библиотеки, перечисленные в requirements.txt,
если этого не произошло, установите их при помощи Python Packages вручную

## Далее команды для терминала Python:

- `cd restapi` (переход в папку restapi)
- `python manage.py migrate` (при помощи файла-мененджера запускается миграция базы данных)
- `python manage.py createsuperuser` (запускается процесс регистрации пользователя, в следующих поля введите ник, почту
  и пароль (два раза))
- `python manage.py runserver` (запуск сервера)

Теперь можно перейти в браузер и API будет доступно по адресу [localhost:8000](localhost:8000)  
Для перехода к панели администратора перейдите по адресу [localhost:8000/admin](localhost:8000/admin)
    