import os
import requests
import redis
import pika

try:
    github_token = os.getenv("GITHUB_TOKEN") 
except KeyError:
    raise Exception("Please set environment variables GITHUB_TOKEN")

github_api_url = 'https://api.github.com/users/{}/starred'
github_params = {'access_token':github_token}

GITHUB_STAR_SET = "Github:Stars:{}"
GITHUB_REPO_KEY = "Github:Repos:{}"

r = redis.Redis()

def is_exists_in_db(sub, repo_id):
    return r.sismember(GITHUB_STAR_SET.format(sub), repo_id)

def add_into_db(sub, starred_repo):
    _id = starred_repo.get('id')
    r.sadd(GITHUB_STAR_SET.format(sub), _id)  #add repo_id's to subscription set
    r.hmset(GITHUB_REPO_KEY.format(_id),{'name':starred_repo['name'],'url':starred_repo['html_url']})    #add repo_name and repo_url to repo_id's hash

def on_request(ch, method, properties, github_sub):
    _url = github_api_url.format(github_sub)

    github_params["page"] = 1

    while True:
        response = requests.get(url=_url,params=github_params).json()

        if not response:
            break

        for repo in response:
            if is_exists_in_db(github_sub, repo):
                break
            else:
                add_into_db(github_sub, repo)

            github_params["page"] += 1

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')

channel.queue_bind(exchange='direct_logs',
                   queue='github_queue',
                   routing_key='github')

channel.basic_consume(on_request, queue='github_queue', no_ack=True)

channel.start_consuming()
