import requests
import pytest

from lib.assertions import Assertions
from lib.base_case import BaseCase

#Ex13 User Agent
class TestUserAgent(BaseCase):

    agent_params = [
        (
            {
            'User-Agent' : 'Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
            'Expected-values' : {'platform' : 'Mobile',
                                'browser' : 'No',
                                'device' : 'Android'
                                }
            }
        ),
        (
            {
            'User-Agent' : 'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
            'Expected-values' : {'platform' : 'Mle',
                                'browser' : 'Chrome',
                                'device' : 'iOS'
                                 }
            }
        ),
        (
            {
            'User-Agent' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Expected-values' : {'platform': 'Googlebot',
                                 'browser': 'Unknown',
                                 'device': 'Unknown'
                                 }
            }
        ),
        (
            {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
            'Expected-values': {'platform': 'Web',
                                'browser': 'Chrome',
                                'device': 'No'}

            }
        ),
        (
            {
            'User-Agent':'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Expected-values': {'platform': 'Mobile',
                                'browser': 'No',
                                'device': 'iPhone'}
            }
        )
    ]

    @pytest.mark.parametrize('user_agent', agent_params)
    def test_user_agent_check(self, user_agent):

        user_agent_dict = dict(user_agent)
        print(user_agent_dict)
        user_agent_value = user_agent_dict['User-Agent']

        # expected values
        expected_platform = user_agent_dict['Expected-values']['platform']
        expected_browser = user_agent_dict['Expected-values']['browser']
        expected_device = user_agent_dict['Expected-values']['device']

        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={"User-Agent": user_agent_value}
        )

        # check platform
        Assertions.assert_json_value_by_name(
            response,
            'platform',
            expected_platform,
            f"User Agent: '{user_agent_value}' expected platform: '{expected_platform}' is not equal to actual platform:"
        )

        # check browser
        Assertions.assert_json_value_by_name(
            response,
            'browser',
            expected_browser,
            f"User Agent: '{user_agent_value}' expected browser: '{expected_browser}' is not equal to actual browser:"
        )

        # check device
        Assertions.assert_json_value_by_name(
            response,
            'device',
            expected_device,
            f"User Agent: '{user_agent_value}' expected device: '{expected_device}' is not equal to actual device:"
        )
