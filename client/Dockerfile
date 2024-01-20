# syntax=docker/dockerfile:1

# check node@14 version support node-sass@5.0.0:
# https://www.npmjs.com/package/node-sass
# https://www.npmjs.com/package/all-node-versions
# or replace node-sass@5.0.0 with sass@1.22.10

# build stage
#FROM node:16.13.0-alpine as build-fe-stage
#RUN apk --no-cache --virtual build-dependencies add python2 make g++
FROM node:16.13.0 as build-fe-stage
#RUN apt-get update || : && apt-get install python -y
RUN mkdir /app
COPY . /app
#COPY package*.json /app
WORKDIR /app

#ENV NODE_ENV=development
#ENV NODE_OPTIONS=--openssl-legacy-provider

#RUN npm install
#RUN yarn
#RUN yarn global add node-gyp@10.0.1
#RUN npm install --global node-gyp@10.0.1
#RUN npm rebuild node-sass
#RUN npm uninstall node-sass
#RUN npm install sass -S -D
RUN yarn install
COPY . .
#RUN yarn run build

# list all files/dirs & modules in Docker Desktop
RUN ls -la
RUN ls -la node_modules

#CMD ["yarn",  "serve", "0.0.0.0:8091"]
CMD ["yarn",  "serve"]

#docker build -t client .
#docker ps
#docker container ls
#docker rm -f <container-name>
#docker run -it -p 8091:8091 client

# ENV NODE_ENV=production

# RUN yarn install
# COPY . .
# RUN yarn run build

# Production stage
#FROM nginx:1.16.1-alpine as production-stage
#COPY --from=build-stage /vue-app/dist /usr/share/nginx/html
#EXPOSE 80
#CMD [ "nginx", "-g", "daemon off;"]