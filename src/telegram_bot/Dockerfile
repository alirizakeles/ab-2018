FROM python:3-alpine

RUN pip install python-telegram-bot requests logging redis

EXPOSE 5000
EXPOSE 6379

COPY bot.py /src/bot.py

WORKDIR /src

ENTRYPOINT ["python", "bot.py"]
