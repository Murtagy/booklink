import random

import requests

localhost = "http://127.0.0.1:8000/"

username = str(random.randint(0, 1000)) + "test2"
r = requests.post(
    localhost + "signup",
    json={
        "company": "Comp",
        "username": username,
        "password": "123",
        "email": str(random.randint(0, 1000)) + "example@example12.com",
    },
)
print(r.text)
token = r.json()["access_token"]
r = requests.get(localhost + "users/me", headers={"Authorization": "Bearer " + token})
assert r.status_code == 200

headers = {"Authorization": "Bearer " + token}

r = requests.post(
    localhost + "token",
    data={
        "username": username,
        "password": "123",
    },
)
print(r.text)
assert r.status_code == 200

r = requests.post(localhost + "worker", headers=headers, json={"name": "Макс", "job_title": "Разработчик"})
print(r.text)

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

r = requests.post(
    localhost + "client_slot/1",
    headers=headers,
    json={
        "name": "nn",
        "slot_type": "busy",
        "from_datetime": "2021-11-01 12:00:00",
        "to_datetime": "2021-11-01 12:00:00",
    },
)
r = requests.post(
    localhost + "client_weekly_slot/1",
    headers=headers,
    json={
        "mo": [["2021-10-21 03:01:01", "2021-10-21 05:01:01"]],
        "tu": None,
        "we": None,
        "th": None,
        "fr": None,
        "st": None,
        "su": None,
    },
)

r = requests.get(
    localhost + "client_availability/1",
    headers=headers,
)
print(r.text)



r = requests.post(
    localhost + "worker_weekly_slot/1",
    headers=headers,
    json={
        "mo": [["2021-10-21 03:01:01", "2021-10-21 05:01:01"]],
        "tu": None,
        "we": None,
        "th": None,
        "fr": None,
        "st": None,
        "su": None,
    },
)
print(r.text)
