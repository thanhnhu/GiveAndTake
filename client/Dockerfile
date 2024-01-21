# syntax=docker/dockerfile:1

# check node@14 version support node-sass@5.0.0:
# https://www.npmjs.com/package/node-sass
# https://www.npmjs.com/package/all-node-versions
# or replace node-sass@5.0.0 with sass@1.22.10

# build stage
# use alpine to reduce the image size
#FROM node:16.13.0 as builder
#RUN apt-get update || : && apt-get install python -y
FROM node:16.13.0-alpine as builder
#RUN apk --no-cache --virtual build-dependencies add python3 make g++
RUN mkdir /app
COPY . /app
#COPY package*.json /app
WORKDIR /app

#ENV NODE_ENV=development
#ENV NODE_OPTIONS=--openssl-legacy-provider

# to reduce image size: combine command + install --no-cache
#RUN npm install cache clean --force
#RUN yarn
#RUN yarn global add node-gyp@10.0.1
#RUN npm install --global node-gyp@10.0.1
#RUN npm rebuild node-sass
#RUN npm uninstall node-sass
#RUN npm install sass -S -D
RUN yarn install && yarn cache clean
#COPY . .
#RUN yarn run build

# list all files/dirs & modules in Docker Desktop
#RUN ls -la && ls -la node_modules

# dev stage
# multiple FROM reduce image size
#FROM node:16.13.0-alpine as dev-stage
#COPY --from=builder /app .
FROM builder as dev-stage
COPY . .
#RUN ls -la
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

# production stage
#FROM nginx:1.16.1-alpine as production-stage
#COPY --from=builder /vue-app/dist /usr/share/nginx/html
#EXPOSE 80
#CMD [ "nginx", "-g", "daemon off;"]