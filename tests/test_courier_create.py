from config.settings import BASE_URL, API_DOCS_URL
from data.generator import generate_courier_data
from utils.allure_helpers import attach_response, attach_request_data
from data.static_data import ERROR_MESSAGES, COURIER_REQUIRED_FIELDS
import allure
import pytest


@allure.feature('Создание курьера')
@allure.link(BASE_URL, name='Ссылка на страницу сайта')
@allure.link(API_DOCS_URL, name='Ссылка на страницу документации API')
class TestCourierCreate:
    @allure.title('Успешное создание курьера')
    @allure.description('Проверка: курьер создаётся, код 201, тело {"ok":true}')
    def test_create_courier_success(self, create_courier_response):
        response, _ = create_courier_response
            
        with allure.step('Проверка кода ответа: 201'):
            assert response.status_code == 201

        with allure.step('Проверка, что ответ содержит {"ok": true}'):    
            assert response.json()['ok']
        

    @allure.title('Нельзя создать двух одинаковых курьеров')
    @allure.description(f"""
                         Проверка1: курьер создаётся, код 201
                         Проверка2: курьер не создается, "code": 409,
                         тело "{ERROR_MESSAGES["duplicate_login"]}"
                        """)
    def test_create_duplicate_courier_fails(self, create_courier_response, courier_client): 
        first_response, data = create_courier_response
            
        with allure.step('Проверка кода ответа: 201'):
            assert first_response.status_code == 201, f"Первый курьер не создан: {first_response.text}"

        with allure.step('Повторная отправка POST-запроса на создание курьера'):
            second_response = courier_client.create_courier(data)
            attach_response(second_response, name_prefix="Повторное создание курьера")

        with allure.step('Проверка кода ответа: 409'): 
            assert second_response.status_code == 409

        with allure.step(f'Проверка кода ответа: "message": "{ERROR_MESSAGES["duplicate_login"]}"'):    
            assert second_response.json()["message"] == ERROR_MESSAGES["duplicate_login"] 



    @allure.title('Создание курьера без обязательного поля (пароль, логин) возвращает ошибку')
    @allure.description(f'Проверка: курьер не создаётся, код 400, тело "{ERROR_MESSAGES["missing_data_create"]}"')
    @pytest.mark.parametrize("missing_field", COURIER_REQUIRED_FIELDS)
    def test_create_courier_missing_field(self, courier_client, missing_field):
        with allure.step('Генерация данных нового курьера'):
            data = generate_courier_data()
            attach_request_data(data, name='Данные курьера')

        with allure.step('Удаление обязательного поля'):    
            del data[missing_field]
            attach_request_data(data, name='Данные курьера')

        with allure.step('Отправка POST-запроса на создание курьера'):
            response = courier_client.create_courier(data)
            attach_response(response, name_prefix="Создание курьера")

        with allure.step('Проверка кода ответа: 400'):
            assert response.status_code == 400

        with allure.step(f'Проверка кода ответа: "message": "{ERROR_MESSAGES["missing_data_create"]}"'): 
            assert response.json()["message"] == ERROR_MESSAGES["missing_data_create"]