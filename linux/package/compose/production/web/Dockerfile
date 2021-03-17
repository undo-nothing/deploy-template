FROM python:3.7

ENV DEBIAN_FRONTEND noninteractive


RUN echo "" > /etc/apt/sources.list
RUN echo "deb http://mirrors.aliyun.com/debian/ jessie main contrib non-free" >> /etc/apt/sources.list && \
        echo "deb-src http://mirrors.aliyun.com/debian/ jessie main contrib non-free" >> /etc/apt/sources.list && \
        echo "deb http://mirrors.aliyun.com/debian-security/ jessie/updates main contrib non-free" >> /etc/apt/sources.list && \
        echo "deb-src http://mirrors.aliyun.com/debian-security/ jessie/updates main contrib non-free" >> /etc/apt/sources.list && \
        # Add aliyun docer-ce source
        echo "deb https://mirrors.aliyun.com/docker-ce/linux/debian jessie stable " >> /etc/apt/sources.lista

#RUN apt-get update

RUN apt-get update && \
    apt-get install -y openssl build-essential  libssl-dev libopenblas-dev \
    netcat


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN  mkdir /app

COPY ./web/{{ DjangoProject }}/requirement.txt /app/requirement.txt
COPY ./compose/production/web/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

WORKDIR /app

ENV PIPENV_VENV_IN_PROJECT 1

RUN pip3 install -r /app/requirement.txt -i https://mirrors.aliyun.com/pypi/simple
run pip3 install gunicorn==20.0.4 -i https://mirrors.aliyun.com/pypi/simple
run pip3 install gevent==21.1.2 -i https://mirrors.aliyun.com/pypi/simple

ENTRYPOINT ["/entrypoint.sh"]
