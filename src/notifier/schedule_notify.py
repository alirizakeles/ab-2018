import redis
import json
import pika
import os

from ulduz.constants import USER_SUGGESTIONS, GITHUB_STAR_KEY, \
    GITLAB_STAR_KEY, TELEGRAM_WORKER_QUEUE, GITHUB_REPO_KEY, \
    EMAIL_SERVICE_QUEUE, SCHEDULE_NOTIFIER_QUEUE

RABBIT_HOST = os.getenv('RABBIT_HOST')
RABBIT_PORT = os.getenv('RABBIT_PORT', 5672)
VIRTUAL_HOST = os.getenv('VIRTUAL_HOST')
RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASSWORD = os.getenv('RABBIT_PASSWORD')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)


r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


def on_request(ch, method, properties, body):
    user = json.loads(body.decode())
    user_suggestion_key = USER_SUGGESTIONS.format(user['email'])
    git_keys = [GITHUB_STAR_KEY.format(sub) for sub in
                user['subscriptions']['github']]
    git_keys.append(
        GITLAB_STAR_KEY.format(sub) for sub in user['subscriptions']['gitlab'])
    if check_empty_set(user_suggestion_key):
        r.sunionstore(dest=user_suggestion_key, keys=git_keys)

    prepare_queue_works(user, user_suggestion_key, user['repoCount'], git_keys)


def check_empty_set(user_suggestion_key):
    return r.scard(user_suggestion_key) == 0


def prepare_queue_works(user, user_suggestion_key, count, git_keys):
    chosen_repo_list = []
    ready_repos_list = []

    if not check_empty_set(user_suggestion_key):
        while count > 0:
            if check_empty_set(user_suggestion_key):
                r.sunionstore(dest=user_suggestion_key, keys=git_keys)
            count -= 1
            chosen_repo_list.append(r.spop(user_suggestion_key))
        for repo in chosen_repo_list:
            repo_key = GITHUB_REPO_KEY.format(repo.decode())
            repo_info = r.hgetall(repo_key)
            decoded_repo_info = {k.decode(): v.decode() for k, v in
                                 repo_info.items()}
            ready_repos_list.append(decoded_repo_info)

        email_dict = {'to': '{}'.format(user['email']),
                      'repos': ready_repos_list}
        if user['telegramId'] is not None:
            telegram_dict = {'to': '{}'.format(user['telegramId']),
                             'repos': ready_repos_list}
            work_telegram = json.dumps(telegram_dict)
            r.lpush(TELEGRAM_WORKER_QUEUE, work_telegram)

        work_email = json.dumps(email_dict)
        r.lpush(EMAIL_SERVICE_QUEUE, work_email)


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

channel.queue_declare(queue=SCHEDULE_NOTIFIER_QUEUE)

channel.queue_bind(exchange='work', queue=SCHEDULE_NOTIFIER_QUEUE,
                   routing_key='schedule_notifier')

channel.basic_consume(on_request, queue=SCHEDULE_NOTIFIER_QUEUE, no_ack=True)

channel.start_consuming()
