import os
import requests
import redis

try:
    github_token = os.getenv("GITHUB_TOKEN")
    github_token = 'b1141d703757e42807c5c6bfc314c99041342a5b'
except KeyError:
    raise Exception("Please set environment variables GITHUB_TOKEN")

github_subs = ['vrct','erdemsahin']
github_api_url = 'https://api.github.com/users/{}/starred'
github_params = {'access_token':github_token}

GITHUB_STAR_SET = "Github:Stars:{}"
GITHUB_REPO_KEY = "Github:Repos:{}"


r = redis.Redis()

def is_exists_in_db(user_star_set, repo_id):
    return r.sismember(user_star_set, repo_id)

def add_into_db(user_star_set, starred_repo):
    _id = starred_repo.get('id')
    r.sadd(user_star_set, _id)  #add repo_id's to subscription set
    r.hmset(GITHUB_REPO_KEY.format(_id),{'name':starred_repo['name'],'url':starred_repo['html_url']})    #add repo_name and repo_url to repo_id's hash

for sub in github_subs:
    _url = github_api_url.format(sub)

    github_params["page"] = 1

    while True:
        response = requests.get(url=_url,params=github_params).json()

        if not response:
            break

        for repo in response:
            if is_exists_in_db(GITHUB_STAR_SET.format(sub), repo):
                break
            else:
                add_into_db(GITHUB_STAR_SET.format(sub), repo)

            github_params["page"] += 1
