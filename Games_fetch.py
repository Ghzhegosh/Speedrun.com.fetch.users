import json

import requests
from ratelimit import rate_limited

file = open("Results.txt", "w")
ONE_MINUTE = 60
useri = ['']


@rate_limited(calls=100, period=ONE_MINUTE)
def parsimSuqa():
    bdds = requests.get("https://www.speedrun.com/api/v1/runs")
    body = json.loads(bdds.text)
    dataBody = body['data']
    userList = ['']
    index = 0
    restart = True
    while restart:
        for i in dataBody:
            index += 1
            urin = i['players']
            for j in urin:
                if j['rel'] == 'user' and userList.count(j['uri']) < 1:
                    userList.append(j['uri'])

        if index == 20:
            pagingBody = body['pagination']
            pagingLinks = pagingBody['links']
            print(pagingLinks)
            if len(pagingLinks) == 1:
                body = json.loads(requests.get((pagingLinks[0])['uri']).text)
                dataBody = body['data']
            if len(pagingLinks) == 2:
                if requests.get((pagingLinks[1])['uri']).status_code == 200:
                    bddy = requests.get((pagingLinks[1])['uri'])
                    body = json.loads(bddy.text)
                    dataBody = body['data']
                if requests.get((pagingLinks[1])['uri']).status_code == 400:
                    return userList

            print('we are working')
            print(len(userList)) #чисто проверял код
            index = 0
        elif index < 20:
            restart = False




useri = parsimSuqa()
for element in useri:
    file.write(element+"\n")
file.close()
print(useri)
