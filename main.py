import sys
from io import BytesIO
import requests
from PIL import Image
import json
import pygame

toponym_to_find = input()
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    print('не найдено')
    sys.exit(1)

json_response = response.json()
with open('response.json', 'w') as file:
    json.dump(json_response, file, ensure_ascii=False)
try:
    coords = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
except Exception:
    print('Адресс не найден')
    sys.exit(1)
x, y = coords

api_server = "http://static-maps.yandex.ru/1.x/"
spn = 0.01
params = {
    'll': f'{x},{y}',
    'spn': f'{spn},{spn}',
    'l': 'sat'
}

response = requests.get(api_server, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = f"map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

map_file = 'map.png'
map_number = 0
pygame.init()
screen = pygame.display.set_mode((600, 450))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(pygame.image.load('map.png'), (0, 0))
    pygame.display.flip()
