import requests
import json

token = 'b1141d703757e42807c5c6bfc314c99041342a5b   '
base_url = 'https://api.github.com/users/{}/starred?access_token={}&page={}'.format('{}',token,'{}')
username = 'ab2018microservices'
page = 1

flag = True

while flag :

    url = base_url.format(username,page)
    response = requests.get(url).json()

    if len(response) == 0:
        flag = False

    else:
        star_dict = {}
        for single_star in response:
            star_dict[single_star['id']] = [single_star['html_url'],single_star['description']]



    page += 1

#stardict is final
