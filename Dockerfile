FROM python
RUN mkdir api
WORKDIR ./api
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
WORKDIR ./restapi
RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 8000
