import asyncio
import aiohttp
import time

start = time.time()


def get_jsons(results):
    list_of_games = open('list_of_games/list_of_games.txt', 'a')
    for result in results:
        # print(result)
        json_body = result.json()
        print(json_body)
        scheme = json_body['data']
        for game in scheme:
            list_of_games.write(f'{game["links"][1]["uri"]}\n')


async def fetch(link, offset, session):
    request = session.get(link.format(offset))
    return request


async def fetch_ratelimit(semaphore, link, offset, session):
    async with semaphore:
        response = await fetch(link, offset, session)
    return response


async def get_responses(semaphore, link):
    async with aiohttp.ClientSession() as session:
        tasks = [await fetch_ratelimit(semaphore, link, offset, session) for offset in range(0, 30000, 20)]
        responses = await asyncio.gather(*tasks)
    return responses


url = 'https://www.speedrun.com/api/v1/games?offset={}'
sem = asyncio.Semaphore(2)
loop = asyncio.get_event_loop()
results = loop.run_until_complete(get_responses(sem, url))
get_jsons(results)
end = time.time()
print(end - start)
