import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup

start = time.time()


async def get_jsons(results, session):
    list_of_games = open('list_of_games/list_of_games.txt', 'a')
    for result in results:
        awaited_result = await result
        json_body = await awaited_result.json()
        scheme = json_body['data']
        for game in scheme:
            list_of_games.write(f'https://www.speedrun.com/api/v1/games/{game["id"]}\n')
    await session.close()
    return


async def get_html():
    list_of_jsons = []
    list_of_games = open('list_of_games/list_of_games.txt', 'r')
    async with aiohttp.ClientSession() as session:
        for each in list_of_games:
            request = session.get(each)
            awaited_request = await request
            json = await awaited_request.json()
            kek = (json['data']['weblink'])
            new_request = session.get(kek)
            keked = await new_request
            print(await keked.text())
        for json in list_of_jsons:
            pass


async def fetch(link, offset, session):
    request = session.get(link.format(offset))
    return request


async def fetch_ratelimit(semaphore, link, offset, session):
    async with semaphore:
        response = await fetch(link, offset, session)
    return response


async def get_responses(semaphore, link):
    session = aiohttp.ClientSession()
    tasks = [await fetch_ratelimit(semaphore, link, offset, session) for offset in range(0, 30000, 1000)]
    return tasks, session


url = 'https://www.speedrun.com/api/v1/games?offset={}&_bulk=yes&max=1000'
sem = asyncio.Semaphore(100)
loop = asyncio.get_event_loop()
# results, session = loop.run_until_complete(get_responses(sem, url))
# # print(results)
# loop.run_until_complete(get_jsons(results, session))
loop.run_until_complete(get_html())
end = time.time()
print(end - start)
