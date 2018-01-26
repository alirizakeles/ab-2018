import redis
import requests

r = redis.Redis()

url = "https://api.github.com/users/{}/starred?page=1"

user = "aliriza"
url = url.format(user)

STAR_SET = "Stars:User:{}".format(user)
REPO_KEY = "Repo:{}"


def is_exists_in_db(star_id):
    return r.sismember(STAR_SET, star_id)


def add_into_db(star):
    _id = star.get('id')
    r.sadd(STAR_SET, _id)
    r.set(REPO_KEY.format(id), star)


page = 1
while True:
    url = "https://api.github.com/users/{}/starred?page={}".format(user, page)
    response = requests.get(url)
    stars = response.json()

    if not stars:
        break

    for repo in stars:
        if is_exists_in_db(repo['id']):
            break
        else:
            add_into_db(repo)

    page += 1
