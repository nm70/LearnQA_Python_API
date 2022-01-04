from json.decoder import JSONDecodeError
import requests

# # 1
# payload = {"name": "User"}
# response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
# print(f"1 step. {response.text}")
#
#
# # 2 parsing response is json format
# response = requests.get("https://playground.learnqa.ru/api/hello", {"name": "User"})
# parser_response_text = response.json()
# print(f"2 step. {parser_response_text['answer']}")
#
# # 3 response is not json format
# response = requests.get("https://playground.learnqa.ru/api/get_text")
# print(f"3 step. {response.text}")
#
# try:
#     parser_response_text = response.json()
#     print(f"3 step. {parser_response_text}")
#
# except JSONDecodeError:
#     print("3 step. Responce is not a JSON format")


# response = requests.get("https://playground.learnqa.ru/api/check_type", params={"param1":"value1"})
# print(response.text)
#
# response = requests.post("https://playground.learnqa.ru/api/check_type", data={"param1":"value1"})
# print(response.text)

# # 200 code
# response = requests.post("https://playground.learnqa.ru/api/check_type")
# print(response.status_code)
#
# #500 code
# response = requests.post("https://playground.learnqa.ru/api/get_500")
# print(response.status_code)
# print(response.text)
#
# # 400 code errors client
# response = requests.post("https://playground.learnqa.ru/api/something")
# print(response.status_code)
# print(response.text)

# # headers
# headers = {"some_header":"123"}
# response = requests.post("https://playground.learnqa.ru/api/show_all_headers", headers=headers)
# print(response.text)
# print(response.headers)


# cookie
payload = {"login":"secret_login", "password":"secret_pass"}
response = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)
print(response.text)
print(response.status_code)
print(response.cookies)
print(dict(response.cookies))
print(response.headers)

# payload = {"login":"secret_login", "password":"secret_pass2"}
# response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)
#
# cookie_value = response1.cookies.get('auth_cookie')
#
# cookies = {}
# if cookie_value is not None:
#     cookies.update({"auth_cookie": cookie_value})
#
# response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
# print(response2.text)

