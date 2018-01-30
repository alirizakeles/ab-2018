import pika
import requests
import redis
import os
from json import loads
from ulduz.constants import GITLAB_API_ENDPOINT, GITLAB_STAR_KEY, \
    GITLAB_REPO_KEY, GITLAB_WORKER_QUEUE

RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_PORT = os.getenv('RABBIT_PORT', 5672)
VIRTUAL_HOST = os.getenv('VIRTUAL_HOST')
RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


PARAMS = {}
PARAMS['starred'] = True
QUEUE_NAME = GITLAB_WORKER_QUEUE
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBIT_HOST,
        virtual_host=VIRTUAL_HOST,
        credentials=pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
    )
)

channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    user_list = loads(body.decode())
    print(user_list)
    get_gitlab_users_starred_repos(user_list=user_list)


def receive_from_queue():
    channel.basic_consume(callback,
                          queue=QUEUE_NAME,
                          no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def get_gitlab_users_starred_repos(user_list):
    for user in user_list:
        responses = requests.get(url=GITLAB_API_ENDPOINT.format(user),
                                 params=PARAMS).json()
        repo_ids = []
        for response in responses:
            repo_ids.append(response['id'])
            star_repo = {
                "name": response['name'],
                "url": response['web_url'],
            }
            r.hmset(name=GITLAB_REPO_KEY.format(response['id']),
                    mapping=star_repo)
        r.sadd(GITLAB_STAR_KEY.format(user), *repo_ids)


if __name__ == '__main__':
    receive_from_queue()
