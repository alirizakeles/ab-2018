from requests import get
import pika
from json import loads

list_of_users = []
GITLAB_API_ENDPOINT = 'https://gitlab.com/api/v4/users/{}/projects'
PARAMS = {}
PARAMS['starred'] = True
QUEUE_NAME = 'gitlab-worker-queue'
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

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
    for user in list_of_users:
        responses = get(url=GITLAB_API_ENDPOINT.format(user), params=PARAMS).json()
        for response in responses:
            print (response['name'])
            print (response['web_url'])

if __name__ == '__main__':
    user_list = receive_from_queue()
    get_gitlab_users_starred_repos(user_list=user_list)
