FROM python:3.8

WORKDIR /home

ENV TELEGRAM_API_TOKEN="1855149406:AAEqKKTNoqzWPwrhgY1Yk4SnovTbRs1PxuU"
ENV TELEGRAM_ACCESS_ID="351021287"


ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install postgres
COPY *.py ./
COPY createdb.postgres ./

ENTRYPOINT ["python", "server.py"]