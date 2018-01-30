FROM python:3-alpine

RUN pip install requests 
RUN pip install redis
RUN pip install pika

COPY worker.py /src/worker.py

WORKDIR /src

ENTRYPOINT ["python", "worker.py"]

