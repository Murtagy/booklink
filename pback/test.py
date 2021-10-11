import random

import requests

localhost = "http://127.0.0.1:8000/"

r = requests.post(
    localhost + "signup",
    json={
        "username": str(random.randint(0, 1000)) + "test2",
        "password": "123",
        "email": str(random.randint(0, 1000)) + "example@example12.com",
    },
)
token = r.json()["access_token"]
r = requests.get(localhost + "users/me", headers={"Authorization": "Bearer " + token})
assert r.status_code == 200


# r = requests.get(localhost + "visit/1")
# print(r.text)

# r = requests.post(
#     localhost + "visit",
#     json={
#         "version": 1,
#         "phone": "375",
#         "email": "email@example.com",
#         "client_id": "cc",  # no validation happens on transfer
#         "services": [],
#         "remind_me": True,
#     },
# )
# print(r.text)

# r = requests.get(localhost+'visits')
# print(r.text)

# r = requests.put(localhost+'visit/5', json={
#     'version': 1,
#     'phone': '375',
#     'client_id': 'cc',
#     'services': [],
#     'email': 'email@example.com',
#     'type': 'type',
#     'remind_me': False,
# })
# print(r.text)

# r = requests.get(localhost+'availability/5')
# print(r.text)

# print('Finished')
