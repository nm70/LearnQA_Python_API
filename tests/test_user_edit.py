from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic('Edit user cases')
class TestUserEdit(BaseCase):

    @allure.description('Test edit just created user (positive)')
    def test_edit_just_created_user(self):
        # 1 REGISTER нового пользователя -  POST

        with allure.step("1. create new user"):
            register_data = self.prepare_registration_data()
            response1 = self.create_user_and_check_status_code(register_data)

        # 2 LOGIN
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }

        with allure.step("2. login with register data"):
            response2 = MyRequests.post("/user/login", data=login_data)
            # в ответ получим куки, токен, id пользователя
            response2_values = self.get_response_values_after_login(response2)

        # EDIT
        # отредактируем данные пользователя - метод PUT
        new_name = "Change Name"
        with allure.step(f"3. edit user 'firtName' = '{new_name}'"):
            response3 = MyRequests.put(f"/user/{response2_values['user_id_from_auth_method']}",
                headers = {'x-csrf-token': response2_values["token"]},
                cookies = {'auth_sid': response2_values["auth_sid"]},
                data = {'firstName': new_name}
            )

        Assertions.assert_status_code(response3, 200)

        # GET получим новые данные пользователя для проверки - метод GET
        with allure.step("4. get new details user"):
            response4 = MyRequests.get(f"/user/{response2_values['user_id_from_auth_method']}",
                headers={'x-csrf-token': response2_values["token"]},
                cookies={'auth_sid': response2_values["auth_sid"]}
            )

        # завалим тест
        # new_name = "Change Name_inv"

        with allure.step("5. assertion new user data saved"):
            Assertions.assert_json_value_by_name(
                response4,
                'firstName',
                new_name,
                f"Wrong 'firstName' of the user after edit. Expected '{new_name}' Actual"
            )


    # Ex17_1
    @allure.description('Test not authorized user can change their data (negative)')
    @allure.title("Test - не авторизированный пользователь может изменить свои данные")
    def test_negative_not_authorized_user_can_change_their_data(self):

        # 1 REGISTER нового пользователя - POST
        register_data = self.prepare_registration_data()
        response1 = self.create_user_and_check_status_code(register_data)

        # 2 EDIT
        # проверим, что невозможно изменить данные этого неавторизованного пользователя - PUT
        # ожидаемый status_code = 400
        data={'firstName': "Change Name",
              'user_id': self.get_json_value(response1, "id")
        }
        response2 = self.edit_user_and_check_status_code(data, 400)
        assert response2.content.decode('utf-8') == 'Auth token not supplied', \
                                                   "Not authorized user can change their data"


    # Ex17_2
    @allure.description('Test authorized user can change data another user (negative)')
    def test_negative_authorized_user_can_change_data_another_user(self):

        # 1 REGISTER нового пользователя - POST
        register_data = self.prepare_registration_data()
        response1 = self.create_user_and_check_status_code(register_data)

        # 2 LOGIN
        # залогиниммся c данными только что созданого пользователя - POST
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)


        # 3 вернём данные не авторизированного пользователя и
        # проверим, что пользователь не авторизирован, user_id = 0
        response3 = self.get_not_authorized_user_and_check_that_the_user_ID_is_zero(2)

        # EDIT
        # отредактируем данные пользователя - метод PUT
        data = {'firstName': "Change Name",
                'user_id': 0
        }
        response4 = self.edit_user_and_check_status_code(data, 400)
        assert response4.content.decode('utf-8') == 'Auth token not supplied', \
                                                   "Authorized user can change data another user"


    # Ex 17_3
    @allure.description('Test authorized user can change his email to a new email without dog (negative)')
    # Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем,
    # на новый email без символа @
    def test_negative_authorized_user_can_change_his_email_to_a_new_email_without_dog(self):

        # 1 REGISTER нового пользователя -  POST
        register_data = self.prepare_registration_data()
        response1 = self.create_user_and_check_status_code(register_data)

        # 2 LOGIN
        # залогиниммся c данными только что созданого пользователя - POST
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        # в ответ получим куки, токен, id пользователя
        response2_values = self.get_response_values_after_login(response2)

        # EDIT
        # отредактируем данные пользователя - метод PUT
        new_email = str(register_data['email']).replace('@', '')

        response3 = MyRequests.put(f"/user/{response2_values['user_id_from_auth_method']}",
            headers = {'x-csrf-token': response2_values["token"]},
            cookies = {'auth_sid': response2_values["auth_sid"]},
            data = {'email': new_email}
        )

        Assertions.assert_status_code(response3, 400)
        assert response3.content.decode('utf-8') == 'Invalid email format', \
                                                   "Can edit 'email' to format without '@'"


    # Ex17_4
    @allure.description('Test authorized user can change his "first_name" to a one char value (negative)')
    # пытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем,
    # на очень короткое значение в один символ
    def test_negative_authorized_user_can_change_his_first_name_to_a_one_char_value(self):
        # 1 REGISTER нового пользователя -  POST
        register_data = self.prepare_registration_data()
        response1 = self.create_user_and_check_status_code(register_data)

        # 2 LOGIN
        # залогиниммся c данными только что созданого пользователя - POST
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        # в ответ получим куки, токен, id пользователя
        response2_values = self.get_response_values_after_login(response2)

        # 3 EDIT
        # отредактируем данные пользователя - PUT
        response3 = MyRequests.put(f"/user/{response2_values['user_id_from_auth_method']}",
            headers = {'x-csrf-token': response2_values["token"]},
            cookies = {'auth_sid': response2_values["auth_sid"]},
            data = {'firstName': 'q'}
        )

        Assertions.assert_status_code(response3, 400)
        assert response3.content.decode('utf-8') == '{"error":"Too short value for field firstName"}', \
                                                   "Can edit 'firstName' to a one character value"