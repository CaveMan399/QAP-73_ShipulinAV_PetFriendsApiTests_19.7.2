from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_invalid_email(email='', password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате нет ключа key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_invalid_password(email=valid_email, password='1111111'):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате нет ключа key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_invalid_key(filter=''):
    """ Проверяем что запрос всех питомцев с неправильным ключем auth_key возвращает статус 403.
    Резульнат при этом не содержит списка животных. """

    auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729"}
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403
    assert 'pets' not in result


def test_add_new_pet_with_invalid_auth_key(name='Вжик', animal_type='мух',
                                     age='2', pet_photo='images/fly.jpeg'):
    """Проверяем невозможность добавление питомца с некорректным ключем auth_key"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Задаем заведомо неправильный ключ api
    auth_key = {"key": "ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae729"}

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    assert name not in result


def test_add_new_pet_with_invalid_data_age(name='Вжик', animal_type='мух',
                                     age='999999999999999999999999999999999999999999999',
                                     pet_photo='images/fly.jpeg'):
    """Проверяем невозможность добавление питомца с некорректным данными (возраст)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert name not in result

def test_add_new_pet_with_invalid_data_name(name='', animal_type='мух',
                                     age='1',
                                     pet_photo='images/fly.jpeg'):
    """Проверяем невозможность добавление питомца с некорректным данными (пустое имя)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert name not in result


def test_unsuccessful_delete_self_pet_with_invalid_auth_key():
    """Проверяем невозможность удаления питомца с некорректным ключем"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Вжик", "мух", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление с некорректным ключем
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet({"key": "auth_key"}, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 403 и в списке питомцев присутствует id удаляемого питомца
    assert status == 403
    assert pet_id == my_pets['pets'][0]['id']


def test_unsuccessful_update_self_pet_info_with_invalid_auth_key(name='Вжык', animal_type='мух', age='9'):
    """Проверяем возможность обновления информации о питомце с некорректным ключем"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info({"key": "auth_key"}, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 403
        assert status == 403

        # Ещё раз запрашиваем список своих питомцев и проверяем, что  возраст питомца не изменился
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert age != my_pets['pets'][0]['age']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo_with_invalid_auth_key(name='Вжик', animal_type='мух',
                                     age='7'):
    """Проверяем что нельзя добавить питомца с некорректными ключем"""

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo({"key": "auth_key"}, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert my_pets['pets'][0]['age'] != age


def test_add_photo_of_pet_with__with_invalid_auth_key(pet_photo='images/fly.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца без фотографии и запрашиваем список своих питомцев
    pf.add_new_pet_without_photo(auth_key, "Вжик", "мух", "5")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")


    # Берём id первого питомца из списка и отправляем запрос на добавление фотографии
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.add_photo_of_pet({"key": "auth_key"}, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

    # Снова запрашиваем список своих питомцев и проверяем наличие фотографии
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert my_pets['pets'][0]['pet_photo'] == ''