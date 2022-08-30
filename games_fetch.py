import asyncio
import aiohttp
import time

from aiolimiter import AsyncLimiter
from retry import retry

start = time.time()


async def get_jsons(result):
    list_of_games = open('list_of_games/list_of_games.txt', 'a')
    json_body = await result.json()
    scheme = json_body['data']
    for game in scheme:
        list_of_games.write(f'{game["links"][1]["uri"]} {time.time() - start}\n')


async def fetch(link, offset, session):
    before_request = time.time()
    async with session.get(link.format(offset), timeout=100) as request:
        print(f'{time.time() - before_request} seconds took to get response')
        check = request.status
        # print(request)
        if check == 200:
            print(f'time {time.time() - start}')
            await get_jsons(request)
        elif check != 200:
            print('retrying to get request')
            request = await fetch(link, offset, session)
            print(offset)
            print(f'time {time.time() - start}')


# async def fetch_ratelimit(link, offset, session):
#     response = await fetch(link, offset, session)
#     return response


async def get_responses(link):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(link, offset, session) for offset in range(0, 30000, 20)]
        await asyncio.gather(*tasks)


url = 'https://www.speedrun.com/api/v1/games?offset={}'
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_responses(url))
except asyncio.exceptions.TimeoutError:
    print(f'process stoped at parsing sites after some shit')
# try:
#     loop.run_until_complete(get_jsons())
# except asyncio.exceptions.TimeoutError:
#     print(f'process stoped at getting jsons after{results}')
end = time.time()
print(end - start)
