FROM python:3-alpine

RUN pip install json pika redis schedule threading time

COPY sched.py /src/sched.py

WORKDIR /src

ENTRYPOINT ["python", "sched.py"]
