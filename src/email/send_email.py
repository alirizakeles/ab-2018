import redis
import logging
import os

from ulduz.email.email_service import send_email
from ulduz.constants import EMAIL_SERVICE_QUEUE

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
logger = logging.ERROR
EMAIL_QUEUE = EMAIL_SERVICE_QUEUE


def listen_redis(block=True, timeout=None):
    if block:
        item = r.brpop(EMAIL_QUEUE, timeout=timeout)
    else:
        item = r.rpop(EMAIL_QUEUE)

    if item:
        item = item[1]
    return item


def create_email_body(repo):
    repo_message = "Git Repo Name: {}".format(repo['name'])
    repo_message += "Git Repo Url: {}".format(repo['url'])
    repo_message += '\n'
    return repo_message


if __name__ == '__main__':
    email = listen_redis()
    if type(email) == dict:
        email_body = "************** Git Star Reminder ********************\n"
        for repo in email['repos']:
            email_body += create_email_body(repo)
        email_body += "******************* The End **********************\n"
        send_email(email['to'], email_body)
    else:
        logging.error("There is a non dict type at email_queue")
