import json
import tarfile

import requests

from ratelimit import rate_limited


# fetching_link = 'https://www.speedrun.com/api/v1/games'
# fetching_response = requests.get(fetching_link)
# response_body = json.loads(fetching_response.text)
# scheme_of_pages = response_body['data']
# print(scheme_of_pages[0]['links'][1]['uri'])

# function checks if there is a link to next page with list of games or there is none
ONE_MINUTE=60
@rate_limited(calls=100, period=ONE_MINUTE)
def existance_of_next_link(existent_link):
    fetching_response = requests.get(existent_link)
    response_body = json.loads(fetching_response.text)
    scheme_of_pages = response_body['pagination']
    links_in_scheme = scheme_of_pages['links']
    amount_of_links_in_scheme = len(scheme_of_pages['links'])

    # далее проверка того что ссылка ведёт на следующую страницу, если их 2 то, то что одна из ссылок является следующей
    if amount_of_links_in_scheme == 1 and (links_in_scheme[0])['rel'] == 'next':
        existent_link = (links_in_scheme[0])['uri']
        return existent_link
    elif amount_of_links_in_scheme == 2 and (links_in_scheme[1])['rel'] == 'next':
        existent_link = (links_in_scheme[1])['uri']
        return existent_link
    elif amount_of_links_in_scheme == 1 and (links_in_scheme[0])['rel'] == 'prev':
        return None


def fetching_process(existent_link):
    links_to_runs = []
    while existent_link is not None:
        fetching_response = requests.get(existent_link)
        response_body = json.loads(fetching_response.text)
        scheme_of_body = response_body['data']
        for game in scheme_of_body:
            links_to_runs.append(game['links'][1]['uri'])
        existent_link = existance_of_next_link(existent_link)
    return links_to_runs


runs_list = fetching_process('https://www.speedrun.com/api/v1/games')
file = open("Results.txt", "w")
for element in runs_list:
    file.write(element + "\n")
file.close()
