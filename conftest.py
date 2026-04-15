import pytest
from api_clients.courier_client import CourierClient
from data.generator import generate_courier_data
import allure
from utils.allure_helpers import attach_request_data, attach_response


@pytest.fixture
def courier_client():
    return CourierClient()

@pytest.fixture
def create_courier_response(courier_client):
    #Фикстура для создания курьера с логированием в Allure.
        with allure.step('Сгнерироать данные для нового курьера'):
            data = generate_courier_data()
            attach_request_data(data, name='Данные курьера')

        with allure.step('Отправка POST-запроса на создание курьера'):
            response = courier_client.create_courier(data)
            attach_response(response, name_prefix="Создание курьера")
        return response, data

@pytest.fixture
def registered_courier(courier_client, create_courier_response):
    #Фикстура для создания курьера с логированием в Allure и удаление созданного курьера в конце теста
    response, data = create_courier_response
    
    with allure.step('Провеить успешное создание курьера'):    
        assert response.status_code == 201
    
    with allure.step('Получить id курьера через логин'):   
        login_resp = courier_client.login_courier(data["login"], data["password"])
        courier_id = login_resp.json()["id"]
    
    yield data  
    
    with allure.step('Удалить созданного курьера'):
        courier_client.delete_courier(courier_id)

