
import requests


def cords_to_address(x: int, y: int):
    geocoder_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={str(y)},{str(x)}&format=json"

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()

        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["description"]
        # Координаты центра топонима:
        return toponym_address
    else:
        return 'Error'


def adres_from_adres(address: str):
    try:
        geocoder_request = f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={address}&format=json"

        # Выполняем запрос.
        response = requests.get(geocoder_request)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            # Получаем первый топоним из ответа геокодера.
            # Согласно описанию ответа, он находится по следующему пути:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Полный адрес топонима:
            status = False
            try:
                toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]['Country']['AdministrativeArea']['Locality']['LocalityName']
                full_address = \
                toponym["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]['Country']['AddressLine']
                status = True
            except:
                pass
            if not status:
                try:
                    toponym_address = \
                    toponym["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]['Country']['AdministrativeArea']['SubAdministrativeArea'][
                        'Locality']['LocalityName']
                    full_address = \
                        toponym["metaDataProperty"]["GeocoderMetaData"]["AddressDetails"]['Country']['AddressLine']
                    status = True
                except:
                    pass
            if not status:
                try:
                    toponym_address = \
                        toponym["name"]
                    full_address = f'{toponym_address}, {toponym["description"]}'
                    status = True
                except:
                    pass

            if not status:
                try:
                    toponym_address = \
                        toponym["name"]
                    full_address = toponym_address
                    status = True
                except:
                    return 'Error'
            latitude = str(toponym['Point']['pos']).split(' ')[0]
            longitude = str(toponym['Point']['pos']).split(' ')[1]
            return toponym_address, latitude, longitude, full_address
        else:
            return 'Error'
    except:
        return 'Error'


