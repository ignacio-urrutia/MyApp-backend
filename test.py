import requests

BASE = "http://127.0.0.1:5000/"

data = [
    {"name": "Ignacio", "email": "ignacio@test.cl"},
    {"name": "Fernando", "email": "fernando@test.cl"},
    {"name": "Juan", "email": "jaun@test.cl"}
]

for i in range(len(data)):
    reponse = requests.post(BASE + "user/" + str(i), json=data[i])
    print(reponse.json())

input()

# reponse = requests.post(BASE + "group_chat", json={"name": "Grupo 1", "north_boundary": 1.0, "south_boundary": 2.0, "east_boundary": 3.0, "west_boundary": 4.0, "description": "Grupo 1", "owner_id": 0})
# print(reponse.json())

# Add user 1 to group chat 1
response = requests.put(BASE + "group_chat/3", json={"user_id": 0})
print(response.json())
