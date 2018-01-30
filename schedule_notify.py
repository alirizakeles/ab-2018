import redis
import json
import random
import pika


r = redis.Redis()

def on_request(ch, method, properties, body):
    user = json.loads(body.decode())
    user_suggestion_key = 'User:Suggestions:{}'.format(user['email'])
    git_keys = ["Github:Stars:{}".format(sub) for sub in user['subscriptions']['github']]
    git_keys.append("Gitlab:Stars:{}".format(sub) for sub in user['subscriptions']['gitlab'])
    if check_empty_set(user_suggestion_key):
        r.sunionstore(dest=user_suggestion_key, keys=git_keys)

    prepare_queue_works(user, user_suggestion_key,user['repoCount'], git_keys)


def check_empty_set(user_suggestion_key):
    if len(r.smembers(user_suggestion_key)) == 0:
        flag = True
    else:
        flag = False

    return flag

def prepare_queue_works(user, user_suggestion_key, count, git_keys):
    chosen_repo_list = []
    ready_repos_list = []

    if len(r.smembers(user_suggestion_key)) != 0 :
        while count > 0:
            if check_empty_set(user_suggestion_key) :
                r.sunionstore(dest=user_suggestion_key, keys=git_keys)
            count -= 1
            chosen_repo_list.append(r.spop(user_suggestion_key))
        for repo in chosen_repo_list:
            repo_key = "Github:Repos:{}".format(repo.decode())
            repo_info = r.hgetall(repo_key)
            decoded_repo_info = {k.decode(): v.decode() for k, v in repo_info.items()}
            ready_repos_list.append(decoded_repo_info)


        email_dict = {'to':'{}'.format(user['email']),'repos':ready_repos_list}
        if user['telegramId'] != None :
                telegram_dict = {'to':'{}'.format(user['telegramId']),'repos':ready_repos_list}
                work_telegram = json.dumps(telegram_dict)
                r.lpush('telegram_queue',work_telegram)

        work_email = json.dumps(email_dict)
        r.lpush('email_queue',work_email)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='work',
                         exchange_type='direct')

channel.queue_declare(queue='schedule_notifier_queue')

channel.queue_bind(exchange='work', queue='schedule_notifier_queue',routing_key='schedule_notifier')

channel.basic_consume(on_request, queue='schedule_notifier_queue', no_ack=True)

channel.start_consuming()
