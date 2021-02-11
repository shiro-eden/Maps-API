from PyQt5.QtWidgets import QInputDialog
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
import requests
import json

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 150, 150)

    def run(self):
        name, ok_pressed = QInputDialog.getText(self, "Введите новое место",
                                                "Введите новое место")
        if ok_pressed:
            return name
        else:
            return None


def change_place(params):
    global searched_flag
    app = QApplication(sys.argv)
    ex = Example()
    place = ex.run()
    if not place:
        return params
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": place,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print('не найдено')
        return params

    json_response = response.json()
    with open('response.json', 'w') as file:
        json.dump(json_response, file, ensure_ascii=False)
    try:
        coords = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"][
            "pos"].split()
    except Exception:
        print('Адрес не найден')
        return params
    x, y = coords
    params['ll'] = f'{x},{y}'
    params['pt'] = f'{x},{y},pmwtm1'
    return params


