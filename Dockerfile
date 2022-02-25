FROM python:3-alpine3.10

WORKDIR /home/bot

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python src/main.py