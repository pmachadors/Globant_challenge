import requests
import json

base = 'http://127.0.0.1:5000/'

data = [{'likes': 1123, 'name': 'How to', 'views': 1001}, 
        {'likes': 89312,'name': 'Cook video', 'views': 3124},
        {'likes': 3287, 'name': 'Animal one', 'views': 1895}]

# for i in range(len(data)):
#     response = requests.put(base + 'video/' + str(i), data[i])
#     print(response.json())

# input()

response = requests.get(base + 'video/2')
print(response.json())
