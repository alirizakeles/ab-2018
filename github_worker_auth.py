import requests
import json

token = 'b1141d703757e42807c5c6bfc314c99041342a5b'
base_url = 'https://api.github.com/users/{}/starred?access_token={}&page={}'.format('{}',token,'{}')

def get_stars(username):

    page = 1

    flag = True
    star_dict = {}

    while flag :

        url = base_url.format(username,page)
        response = requests.get(url).json()

        if len(response) == 0:
            flag = False

        else:

            for single_star in response:
                star_dict[single_star['id']] = [single_star['html_url'],single_star['description']]


        page += 1

    print (star_dict)
#stardict is final
