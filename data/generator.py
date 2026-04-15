
import random
import string


# Метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
def generate_random_string(length=10):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

# Генерируем логин, пароль, имя и возвращаем {}
def generate_courier_data():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }
   