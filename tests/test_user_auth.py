import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserAuth(BaseCase):
    # для негативных тестов авторизации без куки или токена
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        # авторизационные данные - словарь
        payload = {
            'email' : 'vinkotov@example.com',
            'password' : '1234'
        }
        # запрос - 1 метод - авторизации залогиниться
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data = payload)

        # проверки
        self.auth_sid = self.get_cookie(response1, 'auth_sid')
        self.token = self.get_header(response1, 'x-csrf-token')
        self.user_id_from_auth_method = self.get_json_value(response1, 'user_id')


    # позитивный тест на авторизацию
    def test_auth_user(self):

        # запрос - 2- метод проверить user_id из первого метода
        response2 = requests.get(
            "https://playground.learnqa.ru/api/user/auth",
            headers = {"x-csrf-token" : self.token},
            cookies = {"auth_sid" : self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            'user_id',
            self.user_id_from_auth_method,
            'User id from auth method if not equal to User id from check method'
        )


    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",headers = {"x-csrf-token" : self.token})
        else:
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth", cookies = {"auth_sid" : self.auth_sid})

        Assertions.assert_json_value_by_name(
            response2,
            'user_id',
            0,
            f"User authorized with {condition}"
        )

        
