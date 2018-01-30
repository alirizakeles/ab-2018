import json
import redis
import pika
import schedule
import time
import threading
import os
from ulduz.constants import NEW_USER_QUEUE, SCHEDULE_NOTIFIER_QUEUE, \
    GITHUB_WORKER_QUEUE, GITLAB_WORKER_QUEUE

RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_PORT = os.getenv('RABBIT_PORT', 5672)
VIRTUAL_HOST = os.getenv('VIRTUAL_HOST')
RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
p = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBIT_HOST,
        virtual_host=VIRTUAL_HOST,
        credentials=pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
    )
)
sub_ch = p.channel()
sub_ch.exchange_declare(exchange='work', exchange_type='direct')
rest_ch = p.channel()
rest_ch.queue_declare(queue=NEW_USER_QUEUE)

periods = {"daily": 1, "weekly": 7, "monthly": 30}
funcs = {"github": GITHUB_WORKER_QUEUE, "gitlab": GITLAB_WORKER_QUEUE}


def user_callback(ch, method, properties, body):
    user_json = body.decode()
    user_dict = json.loads(user_json)

    r.set("User:{}".format(user_dict["email"]), user_json)

    schedule.every(periods[user_dict['period']]).days.at("10:00").do(
        sub_ch.basic_publish, exchange='work',
        routing_key=SCHEDULE_NOTIFIER_QUEUE, body=user_dict["email"])

    for s in user_dict['subscriptions'].keys():
        for g in user_dict['subscriptions'][s]:
            sub_ch.basic_publish(exchange='work', routing_key=funcs[s], body=g)
            schedule.every(periods[user_dict['period']]).days.at("10:00").do(
                sub_ch.basic_publish,
                exchange='work',
                routing_key=funcs[s],
                body=g
            )


def allektamovikmovik():
        while True:
                schedule.run_pending()
                time.sleep(1)


threading.Thread(target=allektamovikmovik).start()

rest_ch.basic_consume(user_callback, queue=NEW_USER_QUEUE, no_ack=True)
rest_ch.start_consuming()
