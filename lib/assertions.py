from requests import Response
import json

class Assertions:

    @staticmethod
    def assert_json_value_by_name(response: Response, name, exepted_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format. Response text is '{response.text}'"

        assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

        actual_value = response_as_dict[name]
        assert actual_value == exepted_value, f'{error_message} {actual_value}'