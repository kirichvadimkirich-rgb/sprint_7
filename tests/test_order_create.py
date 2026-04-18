from config.settings import BASE_URL, API_DOCS_URL
from utils.allure_helpers import attach_response, attach_request_data
from api_clients.order_client import OrderClient
from data.static_data import COLOR_VARIANTS
from data.generator import generate_order_data
import allure
import pytest


@allure.feature('Создание заказа')
@allure.link(BASE_URL, name='Ссылка на страницу сайта')
@allure.link(API_DOCS_URL, name='Ссылка на страницу документации API')
class TestOrderCreate:
    @allure.title('Успешное создание заказа с различными вариантами цвета.')
    @allure.description('Проверка: заказ создан, код 201, тело {"track": ..}, значение track не пустое')
    @pytest.mark.parametrize("color", COLOR_VARIANTS)
    def test_create_order_with_color_variants_success(self, color):
        order_client = OrderClient()

        with allure.step(f'Сгенерировать данные заказа (цвет: {color})'):
            order_data = generate_order_data(color)
            attach_request_data(order_data, name='Данные заказа')

        with allure.step('Отравить POST-запрос Создание заказа'):
            order_resp = order_client.create_order(order_data)
            attach_response(order_resp, name_prefix="Создание заказа")

        with allure.step('Проверить код ответа: 201'):
            assert order_resp.status_code == 201

        with allure.step('Проверить, что ответ содержит поле track'):    
            assert 'track' in order_resp.json(), "В ответе отсутствует поле track"

        with allure.step('Проверить, что значение track не пустое'):   
            assert order_resp.json()['track'], "Поле track, значение не должно быть пустым"
