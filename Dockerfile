FROM python:3.13-alpine

RUN apk add --no-cache bash

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY orgchat/ /app/orgchat

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .env . 

COPY ./scripts/entrypoint.sh . 

RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
