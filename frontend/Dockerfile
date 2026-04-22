# syntax=docker/dockerfile:1

# check node@14 version support node-sass@5.0.0:
# https://www.npmjs.com/package/node-sass
# https://www.npmjs.com/package/all-node-versions
# or replace node-sass@5.0.0 with sass@1.22.10

# build stage
# use alpine to reduce the image size
#FROM node:16.20.2 AS builder
#RUN apt-get update || : && apt-get install python -y
FROM node:20-alpine AS builder
#RUN apk --no-cache --virtual build-dependencies add python3 make g++
#ENV NODE_ENV=development
#ENV NODE_OPTIONS=--openssl-legacy-provider

# Install curl for health check
RUN apk add --no-cache curl

RUN mkdir /app
WORKDIR /app

# Copy only dependency files first for better layer caching
COPY package.json yarn.lock ./
RUN yarn install --production=false && yarn cache clean && \
    npx update-browserslist-db@latest || true && \
    rm -rf node_modules/.cache ~/.npm/_npx || true

# Copy rest of source
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
CMD ["yarn", "dev", "--host", "0.0.0.0", "--port", "8091"]

# production stage
# ENV NODE_ENV=production
FROM nginx:stable-alpine AS production
# Install gettext for envsubst (substitutes env vars in nginx.conf at runtime)
RUN apk add --no-cache gettext
#COPY --from=builder /app/dist /etc/nginx/html
COPY --from=builder /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
# Copy as template; envsubst will generate the real conf at container start
COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/nginx.conf.template
# Default backend host for k3s — override via env var in Helm/docker-compose
ENV NGINX_BACKEND_HOST=backend.giveandtake.svc.cluster.local:8090

#COPY certs/nginx-selfsigned.crt /etc/ssl/certs/
#COPY certs/nginx-selfsigned.key /etc/ssl/private/
#COPY default-ssl.conf /etc/nginx/conf.d/default-ssl.conf
EXPOSE 8091
EXPOSE 80
# Substitute NGINX_BACKEND_HOST in template, then start nginx
CMD ["/bin/sh", "-c", "envsubst '${NGINX_BACKEND_HOST}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/nginx.conf && nginx -g 'daemon off;'"]

#docker build -t frontend .
#docker build -t frontend --target production .
#docker ps
#docker container ls
#docker rm -f <container-name>
#docker run -it -p 8091:8091 frontend