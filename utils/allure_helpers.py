import allure
import json

def attach_response(response, name_prefix="Ответ"):
    #Прикрепляет статус-код и тело ответа к отчёту Allure.
    allure.attach(
        str(response.status_code),
        name=f"{name_prefix} - Код",
        attachment_type=allure.attachment_type.TEXT
    )
    allure.attach(
        response.text,
        name=f"{name_prefix} - Тело",
        attachment_type=allure.attachment_type.JSON
    )

def attach_request_data(data, name="Тело запроса"):
    #Прикрепляет данные запроса (словарь) как JSON.
    allure.attach(
        json.dumps(data, indent=4, ensure_ascii=False),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )