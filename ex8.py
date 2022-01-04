import requests
import time

# Токены

# 1. создать задачу
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
parser_response_text = response.json()
print(parser_response_text)
# print(f"{parser_response_text}  status_code: {response.status_code}")

# 2. делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
payload = {"token" : parser_response_text["token"]}
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=payload)
parser_response_text_2 = response.json()
print(parser_response_text_2)
assert(parser_response_text_2["status"] == 'Job is NOT ready'), f'не правильный status: {parser_response_text_2["status"]}'

# 3. ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
time.sleep(parser_response_text["seconds"])

# 4. делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и наличии поля result
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=parser_response_text)
parser_response_text_4 = response.json()
print(parser_response_text_4)
assert(parser_response_text_4["result"] == '42'), f"фактическмй result: {parser_response_text_4['result']}, ожидаемый result '42'"
assert(parser_response_text_4["status"] == 'Job is ready'), f"фактическмй status: {parser_response_text_4['status']}, ожидаемый status 'Job is ready'"



