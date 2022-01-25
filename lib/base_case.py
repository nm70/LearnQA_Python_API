from lib.assertions import Assertions
from lib.my_requests import MyRequests
import json.decoder
from requests import Response
from datetime import datetime
import string
import random


class BaseCase:

    # получить значение куки
    def get_cookie(self, response: Response, cookie_name):
        # проверим что куки есть в ответе
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]


    # получить значение заголовка
    def get_header(self, response: Response, header_name):
        # проверим что заголовок есть в ответе
        assert header_name in response.headers, f"Cannot find header with name {header_name} in the last response"
        return response.headers[header_name]


    # получить значение ключа из JSON формата
    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()

        except json.decoder.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        return response_as_dict[name]


    # получить данные ответа логина
    def get_response_values_after_login(self, response: Response):
        return {
            "auth_sid" :self.get_cookie(response, 'auth_sid'),
            "token" : self.get_header(response, 'x-csrf-token'),
            "user_id_from_auth_method" : self.get_json_value(response, 'user_id')
        }


    # подготовка регистрационных данных
    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime('%m%D%Y%H%M%S')
            email = f"{base_part}{random_part}@{domain}"
        return {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }


    def get_random_string(self, expected_len: int = 1):
        letters = string.ascii_letters
        random_data = ''.join(random.choice(letters) for i in range(expected_len))
        return random_data


    def print_response(self, response: Response):
        print("\nResponse:")
        print(f"Status code: {response.status_code}")
        print(f"URL: {response.url}")
        print(f"Content: {response.content}")
        print(f"Headers: {response.headers}")
        print(f"Cookies: {response.cookies}")
        print(f"Text: {response.text}")


    def create_user_and_check_status_code(self, data: dict):
        response = MyRequests.post("/user", data=data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")
        return response


    def edit_user_and_check_status_code(self, data: dict, expected_status_code: int = 200):
        response = MyRequests.put(f"/user/{data['user_id']}", data=data)
        Assertions.assert_status_code(response, expected_status_code)
        return response


    def get_not_authorized_user_and_check_that_the_user_ID_is_zero(self, id: int = 2):
        #1 вернём данные не авторизированного пользователя
        response= MyRequests.get(f"/user/{id}")

        #проверим, что пользовател не авторизирован, получим user_id = 0
        response2= MyRequests.get(f"/user/auth")
        Assertions.assert_json_value_by_name(response2, 'user_id', 0, "User authorized")
        return response