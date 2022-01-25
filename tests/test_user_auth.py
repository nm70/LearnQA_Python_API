import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic('Authorization cases')
class TestUserAuth(BaseCase):

    # для негативных тестов авторизации без куки или токена
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        with allure.step('set registration data with "email" and "password"'):
            payload = {'email' : 'vinkotov@example.com', 'password' : '1234'}

        with allure.step('login with registration data'):
            self.response1 = MyRequests.post("/user/login", data = payload)

        # для проверки в ответ получим куки, токен, id пользователя
        self.response1_values = self.get_response_values_after_login(self.response1)


    @allure.description('This test seccessfully authorize user by email and password (positive)')
    @allure.severity('BLOCKER')
    def test_auth_user(self):

        with allure.step(f'Get user id you are authorizes as OR get 0 if not authorized'):
            response2 = MyRequests.get("/user/auth", headers = {"x-csrf-token" : self.response1_values['token']},
                cookies = {"auth_sid" : self.response1_values['auth_sid']})

        Assertions.assert_json_value_by_name(
            response2,
            'user_id',
            self.response1_values['user_id_from_auth_method'],
            'User id from auth method if not equal to User id from check method'
        )


    @allure.description('This test checks authorization status w/o send cookies or token')
    @allure.severity('BLOCKER')
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

        
