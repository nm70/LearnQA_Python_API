from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):

    def test_edit_just_created_user(self):
        # REGISTER нового пользователя - метод POST
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        # залогиниммся c данными только что созданого пользователя - метод POST
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        #  в ответ получим куки, токен, id пользователя
        response2_values = self.get_response_values_after_login(response2)

        # EDIT
        # отредактируем данные пользователя - метод PUT
        new_name = "Change Name"

        response3 = MyRequests.put(f"/user/{response2_values['user_id_from_auth_method']}",
            headers={'x-csrf-token': response2_values["token"]},
            cookies={'auth_sid': response2_values["auth_sid"]},
            data={'firstName': new_name}
        )
        Assertions.assert_status_code(response3, 200)

        # GET получим новые данные пользователя для проверки - метод GET
        response4 = MyRequests.get(f"/user/{response2_values['user_id_from_auth_method']}",
            headers={'x-csrf-token': response2_values["token"]},
            cookies={'auth_sid': response2_values["auth_sid"]}
        )

        # завалим тест
        # new_name = "Change Name_inv"

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            f"Wrong 'firstName' of the user after edit. Expected '{new_name}' Actual"
        )