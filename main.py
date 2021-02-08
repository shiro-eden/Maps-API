import sys
from io import BytesIO
import requests
from PIL import Image
import json
import pygame
from Button import Button
from save_map_image import save_map_image
from GameParameter import display, fps, clock
from PyQt5.QtWidgets import QInputDialog
from change_place import change_place


def change_view():
    global params, map_file
    if params['l'] == 'sat':
        params['l'] = 'map'
    elif params['l'] == 'map':
        params['l'] = 'sat,skl'
    elif params['l'] == 'sat,skl':
        params['l'] = 'sat'
    save_map_image(map_file, params)


def show_change_place():
    global params
    params = change_place(params)
    save_map_image(map_file, params)


toponym_to_find = 'Саратов'
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
    'l': 'sat',
    'pt': ''
}
map_file = 'map.png'
save_map_image(map_file, params)

pygame.init()
running = True
change_view_btn_image = [pygame.transform.scale(pygame.image.load('button_view.png'), (100, 50))]
change_view_btn = Button(10, 10, 100, 100, '', change_view_btn_image, func=change_view)
change_place_btn_image = [pygame.transform.scale(pygame.image.load('button_view.png'), (100, 50))]
change_place_btn = Button(300, 10, 100, 100, '', change_place_btn_image, func=show_change_place)
show_change_place()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(params)
            if event.key == pygame.K_UP:
                spn = float(params['spn'].split(',')[0])
                x, y = [float(i) for i in params['ll'].split(',')]
                y += spn
                if x > 90:
                    x -= spn
                if x < -90:
                    x += spn
                y = y % 180
                params['ll'] = f'{x},{y}'
            if event.key == pygame.K_DOWN:
                x, y = [float(i) for i in params['ll'].split(',')]
                y -= spn
                if x > 90:
                    x -= spn
                if x < -90:
                    x += spn
                y = y % 180
                params['ll'] = f'{x},{y}'
            if event.key == pygame.K_LEFT:
                x, y = [float(i) for i in params['ll'].split(',')]
                x -= spn
                if x > 90:
                    x -= spn
                if x < -90:
                    x += spn
                y = y % 180
                params['ll'] = f'{x},{y}'
            if event.key == pygame.K_RIGHT:
                x, y = [float(i) for i in params['ll'].split(',')]
                x += spn
                if x > 90:
                    x -= spn
                if x < -90:
                    x += spn
                y = y % 180
                params['ll'] = f'{x},{y}'

            save_map_image(map_file, params)
    display.blit(pygame.image.load(map_file), (0, 0))
    change_view_btn.draw(10, 10)
    change_place_btn.draw(300, 10)
    pygame.display.flip()
