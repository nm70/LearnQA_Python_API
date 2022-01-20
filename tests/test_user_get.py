from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserGet(BaseCase):

    # тест на просмотр данных не авторизованного пользоватля по id

    # должен возвращать только username
    # долден не возвращать - email, firstName, lastName
    def test_get_user_details_not_auth(self):

        response = MyRequests.get(f"/user/2")

        Assertions.assert_json_has_key(response, 'username')

        excepted_keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response, excepted_keys)


    # тест на просмотр данных авторизованного пользователя
    def test_get_user_details_auth_as_same_user(self):

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # 1 авторизируемся
        response1 = MyRequests.post("/user/login", data = data)

        # 2 в ответ получим куки, токен, id пользователя
        response1_values = self.get_response_values_after_login(response1)

        # 3 Get user info by id
        response2 = MyRequests.get(f"/user/{response1_values['user_id_from_auth_method']}",
            headers={'x-csrf-token': response1_values["token"]},
            cookies={'auth_sid': response1_values["auth_sid"]}
        )

        excepted_keys = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, excepted_keys)



    # Ex 16
    # тест, для авторизованного пользователя получить данные другого неавторизованного пользователя
    # должен возвращать только username
    # долден не возвращать - email, firstName, lastName

    def test_get_for_authorized_user_details_of_another_unauthorized_user(self):

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # 1 авторизируемся
        response1 = MyRequests.post("/user/login", data = data)

        #в ответ получим куки, токен, id пользователя
        response1_values = self.get_response_values_after_login(response1)

        # 2 проверим, что пользовател авторизирован, получим user_ID
        response2= MyRequests.get(f"/user/auth",
            headers = {"x-csrf-token" : response1_values['token']},
            cookies = {"auth_sid" : response1_values['auth_sid']}
        )

        Assertions.assert_json_value_by_name(
            response2,
            'user_id',
            response1_values['user_id_from_auth_method'],
            'User id from auth method if not equal to User id from check method'
        )

        # 3 вернём данные не авторизированного пользователя и
        # проверим, что пользователь не авторизирован, получим user_id = 0
        response3 = self.get_not_authorized_user_and_check_that_the_user_ID_is_zero(1)

        # проверим, что запрос вернул username
        Assertions.assert_json_has_key(response3, 'username')

        # проверим, что запрос не вернул другие данные
        excepted_keys = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_not_keys(response3, excepted_keys)
