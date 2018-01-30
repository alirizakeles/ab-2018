import redis
import json
import random


r = redis.Redis()
github_subs = []

keys = ["Github:Stars:{}".format(sub) for sub in github_subs]
unioned= r.sunion(keys=keys)

chosen_repos = random.sample(unioned,count)
chosen_repo_list = []

for repo in chosen_repos:
    repo_key = "Github:Repos:{}".format(repo.decode())
    repo_info = r.hgetall(repo_key)
    decoded_repo_info = {k.decode(): v.decode() for k, v in repo_info.items()}
    chosen_repo_list.append(decoded_repo_info)

email_dict = {b'to':b'user.email',b'repos':chosen_repo_list}
telegram_dict = {b'to':b'telegram_id',b'repos':chosen_repo_list}
decoded_email_dict = {k.decode(): v.decode() if type(v) is bytes else v for k, v in email_dict.items()}
decoded_telegram_dict = {k.decode(): v.decode() if type(v) is bytes else v for k, v in telegram_dict.items()}

work_email = json.dumps(decoded_email_dict)
work_telegram = json.dumps(decoded_telegram_dict)

r.lpush('email_queue',work_email)
r.lpush('telegram_queue',work_telegram)
