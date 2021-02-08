import sys
from io import BytesIO
import requests
from PIL import Image
import json
import pygame
from save_map_image import save_map_image

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
    print('Адрес не найден')
    sys.exit(1)

x, y = coords
api_server = "http://static-maps.yandex.ru/1.x/"
spn = 0.01
params = {
    'll': f'{x},{y}',
    'spn': f'{spn},{spn}',
    'l': 'sat'
}
map_file = 'map.png'
save_map_image(map_file, params)

pygame.init()
screen = pygame.display.set_mode((600, 450))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                spn = float(params['spn'].split(',')[0])
                x, y = [float(i) for i in params['ll'].split(',')]
                y += spn
                if y > 90:
                    y -= spn
                if y < -90:
                    y += spn
                x = x % 180
                params['ll'] = f'{x},{y}'
            if event.key == pygame.K_DOWN:
                x, y = [float(i) for i in params['ll'].split(',')]
                y -= spn
                if y > 90:
                    y -= spn
                if y < -90:
                    y += spn
                x = x % 180
                params['ll'] = f'{x},{y}'
            if event.key == pygame.K_LEFT:
                x, y = [float(i) for i in params['ll'].split(',')]
                x -= spn
                if y > 90:
                    y -= spn
                if y < -90:
                    y += spn
                x = x % 180
                params['ll'] = f'{x},{y}'
            if event.key == pygame.K_RIGHT:
                x, y = [float(i) for i in params['ll'].split(',')]
                x += spn
                if y > 90:
                    y -= spn
                if y < -90:
                    y += spn
                x = x % 180
                params['ll'] = f'{x},{y}'
            save_map_image(map_file, params)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
