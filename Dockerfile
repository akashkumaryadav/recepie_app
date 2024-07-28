# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get upgrade
RUN apt-get update
RUN apt-get install -y build-essential libpq-dev zlib1g-dev libjpeg-dev
RUN python -m pip install -U --force-reinstall pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

# copy project
COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
