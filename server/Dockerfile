# syntax=docker/dockerfile:1

FROM python:3.7.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
COPY . /app
WORKDIR /app

RUN pip install pipenv
#RUN pipenv install --dev
RUN pipenv install --system --deploy --ignore-pipfile
#RUN pipenv shell
RUN pip install -r requirements.txt
RUN chmod +x *.sh
#RUN python manage.py migrate
#RUN python manage.py loaddata cities
COPY . .

#EXPOSE 8090
#CMD ["python",  "manage.py", "runserver"]
CMD ["python",  "manage.py", "runserver", "0.0.0.0:8090"]

#docker build -t server .
#docker ps
#docker container ls
#docker rm -f <container-name>
#docker run -it -p 8090:8090 server