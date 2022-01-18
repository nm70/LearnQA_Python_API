from requests import Response
import json

class Assertions:

    @staticmethod
    # проверим json имеет ключ и значение
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        actual_value = response_as_dict[name]
        assert actual_value == expected_value, f"{error_message} '{actual_value}'"


    # проверим json имеет ключ
    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"


    # проверим json имеет ключи
    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        for name in names:
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"


    # проверим json не имеет ключ
    @staticmethod
    def assert_json_has_not_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}'. But it's present!"


    # проверим json не имеет ключи
    @staticmethod
    def assert_json_has_not_keys(response: Response, names):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        for name in names:
            assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}'. But it's present!"


    # проверим код ответа сервера соответствует ожидаемому
    @staticmethod
    def assert_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Unexpected status code! Excepted: '{expected_status_code}' Actual: {response.status_code}"
