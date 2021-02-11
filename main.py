import sys
import requests
import json
import pygame
from pprint import pprint
from Button import Button
from PyQt5.QtWidgets import QApplication
from save_map_image import save_map_image
from GameParameter import display, fps, clock
from change_place import change_place
from view_address import FullAddressWidget


def change_view():
    global params, map_file
    if params['l'] == 'sat':
        params['l'] = 'map'
        change_view_btn.text = 'Карта'
    elif params['l'] == 'map':
        params['l'] = 'sat,skl'
        change_view_btn.text = 'Гибрид'
    elif params['l'] == 'sat,skl':
        params['l'] = 'sat'
        change_view_btn.text = 'Спутник'
    save_map_image(map_file, params)


def show_change_place():
    global params, searched_flag
    params = change_place(params)
    save_map_image(map_file, params)
    searched_flag = True


def cancel_res():
    global params, searched_flag
    params['pt'] = ''
    save_map_image(map_file, params)
    searched_flag = False


def view_full_address():
    global widget
    geocoder_params['geocode'] = params['ll']
    request = requests.get(geocoder_api_server, params=geocoder_params).json()
    request = request['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
    address = request['metaDataProperty']['GeocoderMetaData']['Address']['Components']
    arg = ['locality', 'street', 'house', 'metro', 'district']
    res = []
    for i in address:
        if i['kind'] in arg:
            res.append(i['name'])
    app = QApplication(sys.argv)
    widget = FullAddressWidget()
    if searched_flag:
        widget.switch_address(', '.join(res))
    else:
        widget.switch_address('Сначала выберите место')
    widget.show()
    app.exec_()


searched_flag = True
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

show_change_place()
widget_address = None
pygame.init()
running = True
screen = pygame.display.set_mode((900, 450))
btn_image = [pygame.image.load(f'button_{i}.png') for i in range(2)]
change_view_btn = Button(630, 10, 250, 50, 'Спутник', btn_image, func=change_view)
change_place_btn = Button(630, 100, 250, 50, 'Сменить место', btn_image, func=show_change_place)
cancel_place_btn = Button(630, 190, 250, 50, 'Сброс поискового запроса', btn_image, func=cancel_res)
info_btn = Button(630, 280, 250, 50, 'Полный адрес', btn_image, func=view_full_address)
while running:

    screen.fill((47, 49, 54))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            x, y = [float(i) for i in params['ll'].split(',')]
            if event.key == pygame.K_UP:
                spn = float(params['spn'].split(',')[0])
                y += spn
                if y > 90:
                    y -= spn
                if y < -90:
                    y += spn
                if x > 180:
                    x = (x - 180) - 180
                if x < -180:
                    x = 180 - (-x - 180)
            if event.key == pygame.K_DOWN:
                y -= spn
                if y > 90:
                    y -= spn
                if y < -90:
                    y += spn
                if x > 180:
                    x = (x - 180) - 180
                if x < -180:
                    x = 180 - (-x - 180)
            if event.key == pygame.K_LEFT:
                x -= spn
                if y > 90:
                    y -= spn
                if y < -90:
                    y += spn
                if x > 180:
                    x = (x - 180) - 180
                if x < -180:
                    x = 180 - (-x - 180)
            if event.key == pygame.K_RIGHT:
                x += spn
                if y > 90:
                    y -= spn
                if y < -90:
                    y += spn
                if x > 180:
                    x = (x - 180) - 180
                if x < -180:
                    x = 180 - (-x - 180)
            if event.key == pygame.K_PAGEDOWN:
                spn = float(params['spn'].split(',')[0])
                if spn < 45:
                    params['spn'] = f'{spn * 2},{spn * 2}'
            if event.key == pygame.K_PAGEUP:
                spn = float(params['spn'].split(',')[0])
                if spn > 0.000625:
                    params['spn'] = f'{spn / 2},{spn / 2}'
            params['ll'] = f'{x},{y}'
            save_map_image(map_file, params)
    display.blit(pygame.image.load(map_file), (0, 0))
    change_view_btn.draw(710, 25)
    change_place_btn.draw(680, 115)
    cancel_place_btn.draw(632, 205, size=27)
    info_btn.draw(675, 295)
    pygame.display.flip()
