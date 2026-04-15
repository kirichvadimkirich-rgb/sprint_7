from config.settings import BASE_URL, API_DOCS_URL
from utils.allure_helpers import attach_response, attach_request_data
from data.generator import generate_courier_data
from data.static_data import ERROR_MESSAGES_LOGIN, COURIER_REQUIRED_FIELDS
import allure
import pytest

@allure.feature('Логин курьера')
@allure.link(BASE_URL, name='Ссылка на страницу сайта')
@allure.link(API_DOCS_URL, name='Ссылка на страницу документации API')
class TestCourierLogin:
    @allure.title('Успешная авторизация курьера')
    @allure.description('Проверка: курьер авторизировался, код 200, тело {"id"..}, значение id не пустое')
    def test_authorization_courier_success(self, courier_client, create_courier_response):
        _, data = create_courier_response
        
        with allure.step('Отравить POST-запрос авторизация курьера'):
            login_resp = courier_client.login_courier(data["login"], data["password"])
            attach_response(login_resp, name_prefix="Авторизация курьера")

        with allure.step('Проверка кода ответа: 200'):
            assert login_resp.status_code == 200

        with allure.step('Проверить, что ответ содержит поле id'):    
            assert 'id' in login_resp.json(), "В ответе отсутствует поле id"

        with allure.step('Проверить, что значение id не пустое'):   
            assert login_resp.json()['id'], "Поле id не должно быть пустым"

        
    @allure.title('Авторизация курьера без обязательного поля (пароль, логин) возвращает ошибку')
    @allure.description(f'Проверка: курьер не авторизуется, код 400, тело "{ERROR_MESSAGES_LOGIN["missing_data_login"]}"')
    @pytest.mark.parametrize("missing_field", COURIER_REQUIRED_FIELDS)
    def test_authorization_courier_missing_field(self, create_courier_response, courier_client, missing_field):
        _, data = create_courier_response 
        with allure.step('Создаём копию, чтобы не сломать teardown фикстуры'):    
            test_data = data.copy()

        with allure.step('Удаление обязательного поля'):    
            del test_data[missing_field]
            attach_request_data(test_data, name=f'Данные курьера после удаления обязательного поля {missing_field}')

        with allure.step('Извлекаем значения с учётом возможного отсутствия'): 
            login = test_data.get("login", "")
            password = test_data.get("password", "")

        with allure.step('Отравить POST-запрос авторизация курьера'):
            login_resp = courier_client.login_courier(login, password)
            attach_response(login_resp, name_prefix="Авторизация курьера")

        with allure.step('Проверка кода ответа: 400'):
            assert login_resp.status_code == 400

        with allure.step(f'Проверка кода ответа: "message": "{ERROR_MESSAGES_LOGIN["missing_data_login"]}"'): 
            assert login_resp.json()["message"] == ERROR_MESSAGES_LOGIN["missing_data_login"]


    @allure.title('Авторизация курьера с несуществующей парой (пароль, логин), возвращает ошибку')
    @allure.description(f'Проверка: курьер не авторизуется, код 404, тело "{ERROR_MESSAGES_LOGIN["non_existent_data"]}"')
    @pytest.mark.parametrize("bad_login, bad_password", [
    (True, False),   # неверный логин, верный пароль
    (False, True),   # верный логин, неверный пароль
    (True, True)     # оба неверны
    ])
    def test_create_courier_missing_field(self,create_courier_response, courier_client, bad_login, bad_password):
        _, data = create_courier_response 

        
        with allure.step('Изменить нужные поля'):
            login = data["login"]
            password = data["password"]
            if bad_login:
                login = "bad" + login
            if bad_password:
                password = "bad" + password

        with allure.step('Отправить POST-запрос на авторизацию'):
            login_resp = courier_client.login_courier(login, password)
            attach_response(login_resp, name_prefix="Авторизация с неверными данными")

        with allure.step('Проверка кода ответа: 404'):
            assert login_resp.status_code == 404

        with allure.step(f'Проверка кода ответа: "message": "{ERROR_MESSAGES_LOGIN["non_existent_data"]}"'): 
            assert login_resp.json()["message"] == ERROR_MESSAGES_LOGIN["non_existent_data"]        