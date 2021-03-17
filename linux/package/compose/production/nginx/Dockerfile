# nginx:1.19 latest in 2021-01-18
# refer from https://github.com/nginx-proxy/nginx-proxy/blob/master/Dockerfile
FROM nginx:1.19
LABEL maintainer="test@test.com"

RUN rm -rf /etc/nginx/nginx.conf
COPY ./compose/production/nginx/nginx.conf /etc/nginx/nginx.conf
