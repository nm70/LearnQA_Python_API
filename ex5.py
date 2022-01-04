import json

# распарсить строку

def print_key(key: str, element_dict: dict):
    if key in element_dict:
        print(element_dict[key])
    else:
        print(f"Ключа {key} в JSON нет")


json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'

parser_json_text = json.loads(json_text)
# print(parser_json_text)

# 1 variant
# print(parser_json_text["messages"][1]["message"])
# print(parser_json_text["messages"][1]["timestamp"])

# 2 variant
print_key("message", parser_json_text["messages"][1])
print_key("timestamp", parser_json_text["messages"][1])


