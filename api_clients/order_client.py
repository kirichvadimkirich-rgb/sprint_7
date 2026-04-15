from api_clients.base_client import BaseClient
from config.endpoints import CREATE_ORDER, GET_ORDERS

class OrderClient(BaseClient):
    def create_order(self, order_data):
        return self.post(CREATE_ORDER, json=order_data)

    def get_orders(self, params=None):
        return self.get(GET_ORDERS, params=params)