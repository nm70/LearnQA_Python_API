import requests

# поработать с длинным редиректом

response = requests.get(" https://playground.learnqa.ru/api/long_redirect")
print(response.history)
count_redirect = len(response.history)-1
print(f"Произошло {count_redirect} редиректа")
print(response.url)

