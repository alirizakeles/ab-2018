import os
import requests
import redis
import pika
from ulduz.constants import GITHUB_API_ENDPOINT, GITHUB_STAR_KEY, \
    GITHUB_REPO_KEY, GITHUB_WORKER_QUEUE

RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_PORT = os.getenv('RABBIT_PORT', 5672)
VIRTUAL_HOST = os.getenv('VIRTUAL_HOST')
RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

try:
    github_token = os.getenv("GITHUB_TOKEN") 
except KeyError:
    raise Exception("Please set environment variables GITHUB_TOKEN")

github_api_url = GITHUB_API_ENDPOINT
github_params = {'access_token': github_token}

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def is_exists_in_db(sub, repo_id):
    return r.sismember(GITHUB_STAR_KEY.format(sub), repo_id)


def add_into_db(sub, starred_repo):
    _id = starred_repo.get('id')
    r.sadd(GITHUB_STAR_KEY.format(sub), _id)  #add repo_id's to subscription set
    r.hmset(
        GITHUB_REPO_KEY.format(_id),
        {
            'name': starred_repo['name'],
            'url': starred_repo['html_url'],
        }
    )  # add repo_name and repo_url to repo_id's hash


def on_request(ch, method, properties, github_sub):
    _url = github_api_url.format(github_sub)

    github_params["page"] = 1

    while True:
        response = requests.get(url=_url, params=github_params).json()

        if not response:
            break

        for repo in response:
            if is_exists_in_db(github_sub, repo):
                break
            else:
                add_into_db(github_sub, repo)

            github_params["page"] += 1


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBIT_HOST,
        virtual_host=VIRTUAL_HOST,
        credentials=pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
    )
)

channel = connection.channel()

channel.exchange_declare(exchange='work',
                         exchange_type='direct')

channel.queue_bind(exchange='work',
                   queue='github_queue',
                   routing_key='github')

channel.basic_consume(on_request, queue=GITHUB_WORKER_QUEUE, no_ack=True)

channel.start_consuming()
