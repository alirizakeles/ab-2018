import pika, requests, redis
from json import loads

GITLAB_API_ENDPOINT = 'https://gitlab.com/api/v4/users/{}/projects'
GITLAB_STAR_SET = "Gitlab:Stars:{}"
GITLAB_REPO_KEY = "Gitlab:Repos:{}"

PARAMS = {}
PARAMS['starred'] = True
QUEUE_NAME = 'gitlab-worker-queue'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
r = redis.Redis()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    user_list = loads(body.decode())
    print (user_list)
    get_gitlab_users_starred_repos(user_list=user_list)


def receive_from_queue():
    channel.basic_consume(callback,
                          queue=QUEUE_NAME,
                          no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def get_gitlab_users_starred_repos(user_list):
    for user in user_list:
        responses = requests.get(url=GITLAB_API_ENDPOINT.format(user), params=PARAMS).json()
        repo_ids = []
        for response in responses:
            repo_ids.append(response['id'])
            star_repo = {}
            star_repo['name'] = response['name']
            star_repo['url'] = response['web_url']
            r.hmset(name=GITLAB_REPO_KEY.format(response['id']), mapping=star_repo)
        r.sadd(GITLAB_STAR_SET.format(user), *repo_ids)


if __name__ == '__main__':
    user_list = receive_from_queue()