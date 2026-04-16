from config.settings import BASE_URL, API_DOCS_URL
from utils.allure_helpers import attach_response
from api_clients.order_client import OrderClient
import allure


@allure.feature('Получение списка заказов')
@allure.link(BASE_URL, name='Ссылка на страницу сайта')
@allure.link(API_DOCS_URL, name='Ссылка на страницу документации API')
class TestOrderList:
    @allure.title('Успешное получение списка заказов')
    @allure.description('Проверка: получен список заказов, код 200, тело {"orders": [{}, ...]}')
    def test_get_orders_returns_list(self):  
        order_client = OrderClient()

        with allure.step('Отравить GET-запрос Получение списка заказов'):
            orders_get = order_client.get_orders()
            attach_response(orders_get, name_prefix="Получение списка заказов")

        with allure.step('Проверить код ответа: 200'):
            assert orders_get.status_code == 200

        with allure.step('Проверить, что поле "orders" присутствует'):
            assert 'orders' in orders_get.json(), "Ответ не содержит поле 'orders'"

        with allure.step('Проверить, что поле "orders" список'):
            assert isinstance(orders_get.json()['orders'], list), f"Поле 'orders' должно быть списком, а получен {type(orders_get.json()['orders'])}"

