import time
from json import JSONDecodeError

import requests
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
# from games_fetch import runs_list
import games_fetch
from time import sleep
from retry import retry
import datetime


class Speedrun_Manager:
    def __init__(self):
        self.users = []
        self.broken_games = []

    def param_offset(self, existent_link):
        parsed_url = urlparse(existent_link)
        captured_value = parse_qs(parsed_url.query)['offset'][0]
        return captured_value

    def get_next_page_link(self, link_to_next_page):
        json_body_in_text = requests.get(link_to_next_page)
        response_body = json.loads(json_body_in_text.text)
        scheme_of_pages = response_body['pagination']
        links_in_scheme = scheme_of_pages['links']
        # Variable for check purposes
        amount_of_links_in_scheme = len(scheme_of_pages['links'])
        # далее проверка того что ссылка ведёт на следующую страницу, если их 2 то, то что одна из ссылок является
        # следующей
        if amount_of_links_in_scheme == 1 and (links_in_scheme[0])['rel'] == 'next':
            link_to_next_page = (links_in_scheme[0])['uri']
            print(link_to_next_page + ' 1')
            return link_to_next_page
        elif amount_of_links_in_scheme == 2 and (links_in_scheme[1])['rel'] == 'next' and self.param_offset(
                links_in_scheme[1]['uri']) != '10000':
            print(link_to_next_page + ' 2')
            link_to_next_page = (links_in_scheme[1])['uri']
            return link_to_next_page
        # elif amount_of_links_in_scheme == 2 and self.param_offset(links_in_scheme[1]['uri']) == '10000':
        #     self.broken_games.append(link_to_next_page)
        #     file2 = open(f"broken_games/broken_game.txt", "a")
        #     file2.write(f'{link_to_next_page}\n')
        #     return None
        elif amount_of_links_in_scheme == 1 and (links_in_scheme[0])['rel'] == 'prev':
            return None

    @retry(exceptions=JSONDecodeError)
    def fetching_process(self, existent_link):
        file1 = open("users/user2.txt", "a")
        while existent_link is not None:
            # self.broken_game_check(existent_link)
            time.sleep(0.1)
            fetching_response = requests.get(existent_link)
            response_body = json.loads(fetching_response.text)
            scheme_of_body = response_body['data']
            for run in scheme_of_body:
                if run['players'] and self.users.count(run['players'][0]['uri']) < 1 and (
                        run['players'][0]['rel'] == 'user'):
                    self.users.append(run['players'][0]['uri'])
                    file1.write(f'{run["players"][0]["uri"]}\n')
            if requests.get(existent_link).status_code == 200:
                existent_link = self.get_next_page_link(existent_link)
        return self.users


# Some games have more than 9999 runs which can't be parsed via this algorithm. Cause of API shortcomings
# So we can check if a game is possible to be parsed without going through over 9000 links
def broken_game_check(link_to_games_runs):
    if requests.get(f'{link_to_games_runs}?offset=9980') != 400:
        file2 = open("broken_games/broken_game2.txt", "a")
        file2.write(f'{link_to_games_runs}\n')
        return True
    else:
        return False


print('Starting Fetching of Users' + '\n')
print(datetime.datetime.now())
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
    sleep(0.4)
    print(datetime.datetime.now())

# for user in speedrun_manager.users:
#     file1 = open(f"users/user.txt", "a")
#     file1.write(user + "\n")
#     file1.close()
#     print(user + 'n\n')

# for broken_game in speedrun_manager.broken_games:
#     file2 = open(f"broken_games/broken_game.txt", "a")
#     file2.write(broken_game + "\n")
#     file2.close()
#     print(broken_game + 'n\n')
