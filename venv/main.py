import requests
import json
from ratelimit import rate_limited
from urllib.parse import urlparse
from urllib.parse import parse_qs


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
    elif amount_of_links_in_scheme == 2 and (links_in_scheme[1])['rel'] == 'next' and param_key(links_in_scheme[1]['uri']) != '10000':
        existent_link = (links_in_scheme[1])['uri']
        return existent_link
    elif amount_of_links_in_scheme == 2:
        return None
    elif amount_of_links_in_scheme == 1 and (links_in_scheme[0])['rel'] == 'prev':
        return None

def fetching_process(existent_link):
    links_to_user = []
    while existent_link is not None:
        fetching_response = requests.get(existent_link)
        response_body = json.loads(fetching_response.text)
        scheme_of_body = response_body['data']
        for run in scheme_of_body:
            links_to_user.append(run['players'][0]['uri'])
        if requests.get(existent_link).status_code == 200:
            existent_link = existance_of_next_link(existent_link)
        elif requests.get(existent_link).status_code == 400:
            return links_to_user
    return links_to_user

def param_key(existent_link):
    parsed_url = urlparse(existent_link)
    captured_value = parse_qs(parsed_url.query)['offset'][0]
    return captured_value



list_of_users_links=fetching_process('https://www.speedrun.com/api/v1/runs?game=j1npme6p&offset=9980')
