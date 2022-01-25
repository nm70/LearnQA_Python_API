from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

@allure.epic('Test user delete cases')
class TestUserDelete(BaseCase):

    # Ex 18_1
    # тест не возможно удалить пользователя с ID 2
    @allure.description('Test can not delete user with id 2')
    def test_can_not_delete_user_with_id_2(self):

        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        # 1 LOGIN
        response1 = MyRequests.post("/user/login", data=login_data)
        # в ответ получим куки, токен, id пользователя
        response1_values = self.get_response_values_after_login(response1)

        Assertions.assert_status_code(response1, 200)

        # 2 DELETE
        response2 = MyRequests.delete(f"/user/{response1_values['user_id_from_auth_method']}",
            headers = {'x-csrf-token': response1_values["token"]},
            cookies = {'auth_sid': response1_values["auth_sid"]}
        )

        Assertions.assert_status_code(response2, 400)
        err_string = 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'
        assert err_string in response2.text, "Can delete user by ID 2"


    # Ex 18_2
    # Создать пользователя,
    # авторизоваться из-под него,
    # удалить,
    # затем попробовать получить его данные по ID
    # убедиться, что пользователь действительно удален.

    @allure.description('Test can delete authorized user')
    def test_can_delete_auth_user(self):

        # 1 Create user
        register_data = self.prepare_registration_data()

        response1 = self.create_user_and_check_status_code(register_data)

        # 2 Logs user into the system
        # залогиниммся c данными только что созданого пользователя - POST
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        # в ответ получим куки, токен, id пользователя
        response2_values = self.get_response_values_after_login(response2)

        # 3 Delete user by id (must be logged in as this user)
        response3 = MyRequests.delete(f"/user/{response2_values['user_id_from_auth_method']}",
            headers = {'x-csrf-token': response2_values["token"]},
            cookies = {'auth_sid': response2_values["auth_sid"]}
        )

        # # 4 Get user info by id
        response4 = MyRequests.get(f"/user/{response2_values['user_id_from_auth_method']}",
            headers={'x-csrf-token': response2_values["token"]},
            cookies={'auth_sid': response2_values["auth_sid"]}
        )

        Assertions.assert_status_code(response4, 404)
        assert response4.text == 'User not found', 'Deleted user found !'


    # Ex18_3
    # залогиниться
    # создать полльзователя
    # удалить данные, только что созданного пользователя,
    @allure.description('Test authorized user can delete data another user (negative)')
    def  test_negative_authorized_user_can_delete_data_another_user(self):

        # 1 LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        # 2 Create
        register_data = self.prepare_registration_data()
        response2 = self.create_user_and_check_status_code(register_data)
        id_create = self.get_json_value(response2, 'id')

        # 3 Delete user by id
        response3 = MyRequests.delete(f"/user/{id_create}"
            # headers = {'x-csrf-token': response2_values["token"]},
            # cookies = {'auth_sid': response2_values["auth_sid"]}
        )

        Assertions.assert_status_code(response3, 400)
        assert 'Auth token not supplied' in response3.text, "Authorized user can delete data another user"

