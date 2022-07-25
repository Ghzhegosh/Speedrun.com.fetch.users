import json
import datetime

import requests

from ratelimit import rate_limited


# fetching_link = 'https://www.speedrun.com/api/v1/games'
# fetching_response = requests.get(fetching_link)
# response_body = json.loads(fetching_response.text)
# scheme_of_pages = response_body['data']
# print(scheme_of_pages[0]['links'][1]['uri'])

# function checks if there is a link to next page with list of games or there is none


def get_next_page_link(existent_link):
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
    # links_to_runs = []
    list_of_games = open('list_of_games/list_of_games.txt', 'a')
    while existent_link is not None:
        fetching_response = requests.get(existent_link)
        response_body = json.loads(fetching_response.text)
        scheme_of_body = response_body['data']
        for game in scheme_of_body:
            # links_to_runs.append(game['links'][1]['uri'])
            list_of_games.write(f'{game["links"][1]["uri"]}\n')
        existent_link = get_next_page_link(existent_link)
        print(existent_link)




file = open('list_of_games/list_of_games.txt', 'r')
if len(file.readlines()) == 0:
    print('checked')
    print(datetime.datetime.now())
    fetching_process('https://www.speedrun.com/api/v1/games?offset=30040')


#runs_list = fetching_process('https://www.speedrun.com/api/v1/games')
# print(len(runs_list))
