# syntax=docker/dockerfile:1

# check node@14 version support node-sass@5.0.0:
# https://www.npmjs.com/package/node-sass
# https://www.npmjs.com/package/all-node-versions
# or replace node-sass@5.0.0 with sass@1.22.10

# build stage
# use alpine to reduce the image size
#FROM node:16.20.2 AS builder
#RUN apt-get update || : && apt-get install python -y
FROM node:16.20.2-alpine AS builder
#RUN apk --no-cache --virtual build-dependencies add python3 make g++
#ENV NODE_ENV=development
#ENV NODE_OPTIONS=--openssl-legacy-provider

# Install curl for health check
RUN apk add --no-cache curl

RUN mkdir /app
COPY . /app
#COPY package*.json /app
WORKDIR /app

# to reduce image size: combine command + install --no-cache
#RUN npm install cache clean --force
#RUN yarn
#RUN yarn global add node-gyp@10.0.1
#RUN npm install --global node-gyp@10.0.1
#RUN npm rebuild node-sass
#RUN npm uninstall node-sass
#RUN npm install sass -S -D
RUN yarn install && yarn cache clean && \
    npx update-browserslist-db@latest || true && \
    rm -rf node_modules/.cache ~/.npm/_npx || true
# Copy files from local machine to virtual directory in docker image
COPY . .
# build into /app/dist
RUN yarn build

# list all files/dirs & modules in Docker Desktop
#RUN ls -la && ls -la node_modules

# development stage
# multiple FROM reduce image size
#FROM node:16.13.0-alpine AS development
#COPY --from=builder /app .
FROM builder AS development
#COPY . .
#CMD ["yarn",  "serve", "0.0.0.0:8091"]
CMD ["yarn", "serve"]

# production stage
# ENV NODE_ENV=production
FROM nginx:stable-alpine AS production
#COPY --from=builder /app/dist /etc/nginx/html
COPY --from=builder /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/

#COPY certs/nginx-selfsigned.crt /etc/ssl/certs/
#COPY certs/nginx-selfsigned.key /etc/ssl/private/
#COPY default-ssl.conf /etc/nginx/conf.d/default-ssl.conf
EXPOSE 8091
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;"]

#docker build -t client .
#docker build -t client --target production .
#docker ps
#docker container ls
#docker rm -f <container-name>
#docker run -it -p 8091:8091 client