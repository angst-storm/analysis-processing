FROM python
ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"
RUN mkdir api
WORKDIR ./api
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
WORKDIR ./restapi
RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 8000
#CMD ["python", "manage.py", "createsuperuser"]
CMD ["python", "manage.py", "runserver"]
