FROM python:3.9.9-alpine

WORKDIR /usr/src/app
RUN mkdir /usr/src/app/static
RUN mkdir /usr/src/app/media

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODDE=1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev gcc python3-dev jpeg-dev zlib-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/app/backend/entrypoint.sh"]