import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='check',
        password='Pushkinz123',
        database='Games',
        cursorclass=pymysql.cursors.DictCursor
    )
    print('succesfull connection')
except Exception as ex:
    print('connection failed')
    print(ex)

with connection.cursor() as cursor:
    create_database_query = "CREATE DATABASE Games"
    create_table = "CREATE TABLE 'games'(id int AUTO_INCREMENT, name varchar(32), linkk varchar(32),PRIMARY_KEY (id))"
    cursor.execute(create_table)
#
# req = requests.get('https://www.speedrun.com/hl2ce')
# html = req.text
# soup = BeautifulSoup(html, "lxml")
#
# GameStatsSidebar = soup.find("div", {"component-name": "GameStatsSidebar"})
# stats_data = GameStatsSidebar.get("component-data")
# if stats_data[-1] == "=":
#     stats_data = stats_data[:-1]
# new_req = requests.get(f'https://www.speedrun.com/api/v2/game/getSummary?_r={stats_data}')
# print(new_req.json()['gameStats'][0]['totalRuns'])
#
#
# async def get_html():
#     list_of_jsons = []
#     list_of_games = open('list_of_games/list_of_games.txt', 'r')
#     async with aiohttp.ClientSession() as session:
#         for each in list_of_games:
#             request = session.get(each)
#             awaited_request = await request
#             json = await awaited_request.json()
#             kek = (json['data']['weblink'])
#             new_request = session.get(kek)
#             keked = await new_request
#             print(await keked.text())
