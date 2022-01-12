import requests
from lib.assertions import Assertions
from lib.base_case import BaseCase

class TestMyExample(BaseCase):

    # Ex10 тест на короткую фразу
    def test_short_phrase(self):

        phrase = input("Set a phrase: ")
        len_phrase = len(phrase)
        assert len_phrase < 15, f"The phrase '{phrase}' is no shorter than 15 characters"


    #Ex11 Тест запроса на метод cookie позитивный
    def test_homework_cookie(self):

        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        # посмотрим
        cookies_dist = dict(response.cookies)
        print(cookies_dist)
        expected_cookie = cookies_dist['HomeWork']

        # проверим ключ и значение
        actual_cookie = self.get_cookie(response, 'HomeWork')
        print(actual_cookie)
        assert actual_cookie == expected_cookie, f"Actual cookie '{actual_cookie}' is not equal to expected cookie '{expected_cookie}'"

        # сломаем проверку
        # expected_cookie = 'invalid'
        # assert actual_cookie == expected_cookie, f"Actual cookie '{actual_cookie}' is not equal to expected cookie '{expected_cookie}'"


    # Ex11 Тест запроса на метод cookie негативный
    # def test_homework_cookie_negative(self):
    #
    #     response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
    #     # проверим
    #     cookie = self.get_cookie(response, 'HomeWork_inv')
    #     print(cookie)


    #Ex12 Тест запроса на метод header позитивный
    def test_homework_header(self):

        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        # посмотрим
        print(response.headers)

        # проверим ключ и значение
        for element_header in response.headers:
            expected_header = response.headers[element_header]

            #проверим ключ
            actual_header = self.get_header(response, element_header)
            print(actual_header)

            # проверим значение
            assert actual_header == expected_header, f"Actual header '{actual_header}' is not equal to expected header '{expected_header}'"


