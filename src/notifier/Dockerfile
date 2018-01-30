FROM python:3.6-alpine

RUN pip install redis pika

EXPOSE 5672 6380

COPY schedule_notify.py /src/schedule_notify.py

WORKDIR /src

ENV RABBIT_HOST=127.0.0.1 \
  RABBIT_PORT=15672 \
  RABBIT_USER=guest \
  RABBIT_PASSWORD=guest \
  RABBIT_VHOST=/

ENTRYPOINT ["python", "schedule_notify.py"]
