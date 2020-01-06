import json

data = json.load(open("data.json"))
data = list(filter(lambda x: x["dot pattern"]=="123456", data))[0]
print(data)