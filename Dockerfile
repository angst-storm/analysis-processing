FROM python
COPY --from=openjdk . ./java
RUN mkdir analysis-processing
WORKDIR ./analysis-processing
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN apt-get update
RUN apt-get install -y python3-opencv
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
WORKDIR ./restapi
RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 8000
