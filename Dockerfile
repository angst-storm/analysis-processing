# установка Python
FROM python
RUN apt-get update && \
    # установка Java
    apt-get install -y openjdk-11-jre-headless && \
    # установка Poppler
    apt-get install poppler-utils -y && \
    # установка Tesseract
    apt-get install tesseract-ocr -y  && \
    apt-get clean
# создание папки для файлов проекта
RUN mkdir analysis-processing
WORKDIR ./analysis-processing
# копирование проекта в коентейнер
COPY . .
# установка библиотек Python
RUN pip install -r ./requirements.txt
WORKDIR ./restapi
# подготовка сервера к запуску
RUN python manage.py migrate
RUN python manage.py collectstatic
# открытие порта
EXPOSE 8000
