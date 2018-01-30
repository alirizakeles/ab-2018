FROM python:3-alpine

RUN pip install falcon
RUN pip install json
RUN pip install redis
RUN pip install pika
RUN pip install os
RUN pip install graceful
RUN pip install gunicorn

EXPOSE 5000

CMD ["gunicorn" , "-b", "0.0.0.0:8888"]
