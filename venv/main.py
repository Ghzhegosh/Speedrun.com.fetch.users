import time

import requests
import json
from ratelimit import rate_limited
from urllib.parse import urlparse
from urllib.parse import parse_qs
from games_fetch import runs_list
from time import sleep
import datetime



class Users:
    def __init__(self,link):
        self.link=link

class Broken_Games:
    def __init__(self,link):
        self.link=link

class Speedrun_Manager:
    def __init__(self):
        self.users=[]
        self.broken_games=[]

    def param_offset(self,existent_link):
        parsed_url = urlparse(existent_link)
        captured_value = parse_qs(parsed_url.query)['offset'][0]
        return captured_value

    def param_game(self,existend_link):
        parsed_url = urlparse(existend_link)
        captured_value = parse_qs(parsed_url.query)['game'][0]
        return captured_value

    def existance_of_next_link(self,existent_link):
        fetching_response = requests.get(existent_link)
        response_body = json.loads(fetching_response.text)
        scheme_of_body = response_body['data']
        scheme_of_pages = response_body['pagination']
        links_in_scheme = scheme_of_pages['links']
        amount_of_links_in_scheme = len(scheme_of_pages['links'])
        # далее проверка того что ссылка ведёт на следующую страницу, если их 2 то, то что одна из ссылок является следующей
        if amount_of_links_in_scheme == 1 and (links_in_scheme[0])['rel'] == 'next':
            existent_link = (links_in_scheme[0])['uri']
            print(existent_link+' 1')
            return existent_link
        elif amount_of_links_in_scheme == 2 and (links_in_scheme[1])['rel'] == 'next' and self.param_offset(links_in_scheme[1]['uri']) != '10000':
            print(existent_link+' 2')
            existent_link = (links_in_scheme[1])['uri']
            return existent_link
        elif amount_of_links_in_scheme == 2 and self.param_offset(links_in_scheme[1]['uri']) == '10000':
            self.broken_games.append(s)
            return None
        elif amount_of_links_in_scheme == 1 and (links_in_scheme[0])['rel'] == 'prev':
            return None


    def fetching_process(self,existent_link):
        while existent_link is not None:
            time.sleep(1)
            fetching_response = requests.get(existent_link)
            response_body = json.loads(fetching_response.text)
            scheme_of_body = response_body['data']
            for run in scheme_of_body:
                if run['players'] and self.users.count(run['players'][0]['uri']) < 1 and (run['players'][0]['rel']== 'user'):
                    self.users.append(run['players'][0]['uri'])
            if requests.get(existent_link).status_code == 200:
                existent_link = self.existance_of_next_link(existent_link)
        return self.users

print('starting sheet'+'\n')
print(datetime.datetime.now())
speedrun_manager=Speedrun_Manager()
file1 = open("Users.txt", "w")
file2 = open("broken_games.txt", "w")
for run in runs_list:
    print(run+'  '+'\n')
    speedrun_manager.fetching_process(run)
    sleep(0.8)
    print(datetime.datetime.now())

for user in speedrun_manager.users:
    file1.write(user + "\n")
    print(user+'n\n')

for broken_game in speedrun_manager.broken_games:
    file2.write(broken_game+"\n")
    print(broken_game + 'n\n')

file1.close()
file2.close()


