FROM python:3.10.6

ENV DockerHome=/code/

RUN mkdir -p %DockerHome

WORKDIR $DockerHome

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $DockerHome

RUN pip install -r requirements.txt

CMD python manage.py runserver
