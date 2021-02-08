import requests
import sys


def save_map_image(map_file, params):
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = f"map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
