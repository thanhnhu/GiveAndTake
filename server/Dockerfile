# syntax=docker/dockerfile:1

# use alpine to reduce the image size
FROM python:3.9-alpine as builder
# use 3.9 instead of 3.7 to use Pillow and JSONField with sqlite3
ENV PYTHONUNBUFFERED 1

# Create the virtual environment.
#RUN python -m venv /venv
#ENV PATH=/venv/bin:$PATH

RUN mkdir /app
COPY . /app
WORKDIR /app

# below for mysqlclient library
RUN apt update && apt install -y \
  default-libmysqlclient-dev \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# to reduce image size: combine command + pip i --no-cache-dir
RUN pip install --no-cache-dir pipenv && \
  #pipenv install --dev
  pipenv install --system --deploy --ignore-pipfile && \
  #pipenv shell
  #pip install --no-cache-dir --upgrade pip
  pip install --no-cache-dir -r requirements.txt && \
  pip cache purge && \
  #python manage.py migrate && \
  #python manage.py loaddata cities && \
  python manage.py collectstatic --noinput && \
  chmod +x *.sh
COPY . .

# list all files/dirs in Docker Desktop
#RUN ls -la

# development stage
FROM builder as development
#EXPOSE 8090
CMD python manage.py runserver 0.0.0.0:8090

# production stage
FROM builder as production
#EXPOSE 8090
CMD gunicorn -b 0.0.0.0:8090 backend.wsgi:application --timeout 600 --reload --log-level=info

#docker build -t server .
#docker ps
#docker container ls
#docker rm -f <container-name>
#docker run -it -p 8090:8090 server
#docker-compose up/down