import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

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
        # запрос - 1 метод - залогиниться
        self.response1 = MyRequests.post("/user/login", data = payload)

        # для проверки в ответ получим куки, токен, id пользователя
        self.response1_values = self.get_response_values_after_login(self.response1)


    # позитивный тест на авторизацию
    def test_auth_user(self):

        # запрос - 2- метод проверить user_id из первого метода
        response2 = MyRequests.get("/user/auth",
            headers = {"x-csrf-token" : self.response1_values['token']},
            cookies = {"auth_sid" : self.response1_values['auth_sid']}
        )

        Assertions.assert_json_value_by_name(
            response2,
            'user_id',
            self.response1_values['user_id_from_auth_method'],
            'User id from auth method if not equal to User id from check method'
        )


    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):

        if condition == "no_cookie":
            response2 = MyRequests.get("/user/auth", headers = {"x-csrf-token" : self.response1_values['token']})
        else:
            response2 = MyRequests.get("/user/auth", cookies = {"auth_sid" : self.response1_values['auth_sid']})

        Assertions.assert_json_value_by_name(
            response2,
            'user_id',
            0,
            f"User authorized with {condition}"
        )

        
