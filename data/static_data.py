

ERROR_MESSAGES_CREATE = {
    "duplicate_login": "Этот логин уже используется. Попробуйте другой.",
    "missing_data_create": "Недостаточно данных для создания учетной записи"
}

ERROR_MESSAGES_LOGIN = {
    "missing_data_login": "Недостаточно данных для входа", 
    "non_existent_data": "Учетная запись не найдена"
}



COURIER_REQUIRED_FIELDS = ["login", "password"]


INVALID_CREDENTIALS_COMBINATIONS  = [
    ("invalidlogin", "valid_password_placeholder"),   # неверный логин, верный пароль
    ("valid_login_placeholder", "invalidpassword"),   # верный логин, неверный пароль
    ("invalidlogin", "invalidpassword")                # оба неверны
]


# Варианты цвета для создания заказа
COLOR_VARIANTS = [
    ["BLACK"],          # один цвет — чёрный
    ["GREY"],           # один цвет — серый
    ["BLACK", "GREY"],  # оба цвета
    []                  # без цвета (пустой список)
]