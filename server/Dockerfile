# syntax=docker/dockerfile:1

# use alpine to reduce the image size
FROM python:3.8-alpine as builder
# use 3.8 instead of 3.7 to fix build Pillow
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
COPY . /app
WORKDIR /app

# to reduce image size: combine command + pip i --no-cache-dir
RUN pip install --no-cache-dir pipenv && \
  #pipenv install --dev
  pipenv install --system --deploy --ignore-pipfile && \
  #pipenv shell
  #pip install --no-cache-dir --upgrade pip
  pip install --no-cache-dir -r requirements.txt && \
  pip cache purge && \
  #python manage.py migrate
  #python manage.py loaddata cities
  chmod +x *.sh
COPY . .

# development stage
FROM builder as development
#COPY . .
# list all files/dirs in Docker Desktop
#RUN ls -la

#EXPOSE 8090
#CMD ["python",  "manage.py", "runserver"]
CMD ["python",  "manage.py", "runserver", "0.0.0.0:8090"]

# production stage
FROM builder as production
#EXPOSE 8090
CMD gunicorn -b 0.0.0.0:8090 backend.wsgi:application --timeout 600 --log-level=info --reload
#CMD ["python",  "backend/wsgi.py", "runserver", "0.0.0.0:8090"]

#docker build -t server .
#docker ps
#docker container ls
#docker rm -f <container-name>
#docker run -it -p 8090:8090 server
#docker-compose up/down