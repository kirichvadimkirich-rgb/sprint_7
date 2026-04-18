from api_clients.base_client import BaseClient
from config.endpoints import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER
import allure

class CourierClient(BaseClient):
    def create_courier(self, courier_data):
        return self.post(CREATE_COURIER, json=courier_data)

    def login_courier(self, login, password):
        return self.post(LOGIN_COURIER, json={"login": login, "password": password})
    
    def delete_courier(self, courier_id):
        id = DELETE_COURIER.format(courier_id)
        return self._send_request("DELETE", id)
    
    def delete_courier_by_credentials(self, login, password):
            login_resp = self.login_courier(login, password)
            if login_resp.status_code == 200:
                courier_id = login_resp.json()["id"]
                return self.delete_courier(courier_id)