import time
from json import JSONDecodeError

import requests
import json
# from games_fetch import runs_list
import games_fetch
from time import sleep
from retry import retry
from datetime import datetime


class Speedrun_Manager:
    def __init__(self):
        self.users = []
        self.broken_games = []

    def get_link_to_next_page(self, link_to_next_page):
        scheme_of_pages = get_json_from_link(link_to_next_page, 'pagination')
        pagination_links = scheme_of_pages['links']
        # Variable for check purposes
        amount_of_links_in_scheme = len(pagination_links)
        # далее проверка того что ссылка ведёт на следующую страницу, если их 2 то, то что одна из ссылок является
        # следующей
        if amount_of_links_in_scheme == 1 and (pagination_links[0])['rel'] == 'next':
            link_to_next_page = (pagination_links[0])['uri']
            print(link_to_next_page + ' 1')
            return link_to_next_page
        elif amount_of_links_in_scheme == 2 and (pagination_links[1])['rel'] == 'next':
            print(link_to_next_page + ' 2')
            link_to_next_page = (pagination_links[1])['uri']
            return link_to_next_page
        elif amount_of_links_in_scheme == 1 and (pagination_links[0])['rel'] == 'prev':
            return None

    @retry(exceptions=JSONDecodeError)
    def fetching_process(self, existent_link):
        start = datetime.now()
        file1 = open("users/user2.txt", "a")
        while existent_link is not None:
            runs = get_json_from_link(existent_link, 'data')
            for run in runs:
                if run['players'] and self.users.count(run['players'][0]['uri']) < 1 and (
                        run['players'][0]['rel'] == 'user'):
                    self.users.append(run['players'][0]['uri'])
                    file1.write(f'{run["players"][0]["uri"]}\n')
            if requests.get(existent_link).status_code == 200:
                existent_link = self.get_link_to_next_page(existent_link)
        print(f'{datetime.now() - start} seconds elapsed in this iteration of function')
        return self.users


# Some games have more than 9999 runs which can't be parsed via this algorithm. Cause of API shortcomings
# So we can check if a game is possible to be parsed without going through over 9000 links
def broken_game_check(link_to_games_runs):
    if get_json_from_link(link_to_games_runs, 'data', param={'offset': 9980}):
        file2 = open("broken_games/broken_game2.txt", "a")
        file2.write(f'{link_to_games_runs}\n')
        print(f'{link_to_games_runs} is broken game')
        return True
    else:
        return False


def get_json_from_link(link, part_of_json, param=None):
    request = requests.get(link, params=param)
    print(f'get request of {link} took {request.elapsed.total_seconds()}')
    json_scheme = json.loads(request.text)[part_of_json]
    return json_scheme


print('Starting Fetching of Users' + '\n')
print(datetime.now())
speedrun_manager = Speedrun_Manager()
games_list = open('list_of_games/list_of_games.txt')
games_list_array = games_list.read().split('\n')
for run in games_list_array:  # runs_list:
    if run == '':
        break
    if broken_game_check(run):
        continue
    print(run + ' ' + '\n')
    speedrun_manager.fetching_process(run)
    print(datetime.now())