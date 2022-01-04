import requests

# Запросы и методы

BASE_URL = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае
response = requests.get(BASE_URL)
print(f"1. ответ: {response.text}")

# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае
response = requests.head(BASE_URL)
print(f"2. ответ: {response.headers}")

# 3.  Делает запрос с правильным значением method. Описать что будет выводиться в этом случае
payload = {"method":"GET"}
response = requests.get(BASE_URL)
print(f"3. ответ: {response.text}")

# 4. Проверяет все возможные сочетания реальных типов запроса и значений параметра method
# список методов
kind_methods = ["GET", "POST", "PUT", "DELETE"]

print('GET')
for method in kind_methods:
    payload = {"method": method}
    response = requests.get(BASE_URL, params=payload)
    print(f"GET: {method}  text: {response.text}  status_code: {response.status_code}")

print('POST')
for method in kind_methods:
    payload = {"method": method}
    response = requests.post(BASE_URL, data=payload)
    print(f"POST: {method}  text: {response.text}  status_code: {response.status_code}")

print('PUT')
for method in kind_methods:
    payload = {"method": method}
    response = requests.put(BASE_URL, data=payload)
    print(f"PUT: {method}  text: {response.text}  status_code: {response.status_code}")

print('DELETE')
for method in kind_methods:
    payload = {"method": method}
    response = requests.delete(BASE_URL, data=payload)
    print(f"DELETE: {method}  text: {response.text}  status_code: {response.status_code}")




