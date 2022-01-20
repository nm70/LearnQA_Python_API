from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest

class TestUserRegister(BaseCase):

    field_names = [
        ("firstName"),
        ("lastName"),
        ("username"),
        ("password")
    ]

    exclude_params = [
        ("no_username"),
        ("no_email"),
        ("no_password")
    ]


    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        self.create_user_and_check_status_code(data)


    # тест негативный на создание пользователя с существующим email
    def test_create_user_with_existing_email(self):

        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data = data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists", \
                                                    f"Unexpected response content {response.content}"


    # Ex 15
    # тест создать пользователя с некорректным email - без символа @
    def test_can_сreate_user_with_an_incorrect_email(self):

        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data = data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"Invalid email format", \
                                                    f"Can create user with an incorrect email '{email}'"


    # Ex15
    # Создание пользователя с очень коротким именем в один символ
    @pytest.mark.parametrize('name', field_names)
    def test_can_create_user_with_single_character_field(self, name):

        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        data[name] = self.get_random_string()

        response = MyRequests.post("/user", data = data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"The value of '{name}' field is too short", \
                                                   f"Can create user with an single character field '{name}' = '{data[name]}'"


    # Ex15
    # Создание пользователя с очень длинным именем в 251 символ
    @pytest.mark.parametrize('name', field_names)
    def test_can_create_user_with_too_long_character_field(self, name):

        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        data[name] = self.get_random_string(251)

        response = MyRequests.post("/user", data = data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"The value of '{name}' field is too long", \
                                                   f"Can create user with a too long character field '{name}' = '{data[name]}'"


    # Ex 15
    # регистрация пользователя без указания одного из полей
    @pytest.mark.parametrize('condition', exclude_params)
    def test_can_create_user_without_params(self, condition):

        data = self.prepare_registration_data()

        if condition == "no_username":
            name = 'username'
        elif condition == "no_email":
            name = 'email'
        else:
            name = 'password'

        data[name] = None

        response = MyRequests.post("/user", data = data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"The following required params are missed: {name}", \
                                                   f"The following required params are missed: '{name}'"


