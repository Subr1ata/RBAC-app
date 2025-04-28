# Use the official Python image as the base image
FROM python:3.11.4-alpine

# Set working directory inside the container
WORKDIR /usr/src/app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# RUN cp -r /usr/src/app /usr/src/app_backup

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app

# Set the entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
