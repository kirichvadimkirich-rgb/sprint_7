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
    #Фикстура создаёт курьера, возвращает (response, data) и удаляет курьера после теста.
        with allure.step('Сгенерироать данные для нового курьера'):
            data = generate_courier_data()
            attach_request_data(data, name='Данные курьера')

        with allure.step('Отправить POST-запрос на создание курьера'):
            response = courier_client.create_courier(data)
            attach_response(response, name_prefix="Создание курьера")
        
        yield response, data

        with allure.step('Получить id и удалить курьера'):
            login_resp = courier_client.login_courier(data["login"], data["password"])
            if login_resp.status_code == 200:
                courier_id = login_resp.json()["id"]
                courier_client.delete_courier(courier_id)

