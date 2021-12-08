import datetime
import random

import requests

localhost = "http://127.0.0.1:8000/"

### CREATE NEW CLIENT
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
CLIENT_ID = r.json()["client_id"]
###

### ASSURE LOGIN
token = r.json()["access_token"]
r = requests.get(localhost + "users/me", headers={"Authorization": "Bearer " + token})
assert r.status_code == 200, r.text

headers = {"Authorization": "Bearer " + token}

r = requests.post(
    localhost + "token",
    data={
        "username": username,
        "password": "123",
    },
)
print(r.text)
assert r.status_code == 200, r.text
###

### Create worker
r = requests.post(
    localhost + "worker",
    headers=headers,
    json={"name": "Макс", "job_title": "Разработчик"},
)
print(r.text)

r = requests.get(
    localhost + "workers",
    headers=headers,
)
print(r.text)
assert len(r.json()) == 1, r.text
WORKER_ID = r.json()[0]["worker_id"]
###

### Create worker (2)
r = requests.post(
    localhost + "worker",
    headers=headers,
    json={"name": "Макс", "job_title": "Разработчик", "use_company_schedule": True},
)
# assert r.status_code == 428

### Create worker (3)
r = requests.post(
    localhost + "worker",
    headers=headers,
    json={"name": "Макс", "job_title": "Разработчик", "use_company_schedule": False},
)
print(r.text)
WORKER_NO_SCHEDULE_ID = r.json()["worker_id"]

### Check workers n
r = requests.get(
    localhost + "workers",
    headers=headers,
)
print(r.text)
assert len(r.json()) == 3
###

### Services
r = requests.post(
    localhost + f"service",
    headers=headers,
    json={
        "name": "Стрижка",
        "price": 13.1,
        # price_lower_bound: Optional[float]
        # price_higher_bound: Optional[float]
        "seconds": 45 * 60,
        "description": "Ножницы, все такое",
    },
)
SERVICE_ID = r.json()["service_id"]

r = requests.get(
    localhost + f"service/{SERVICE_ID}",
)
assert r.json()["service_id"] == SERVICE_ID, r.text


r = requests.get(
    localhost + f"client/{CLIENT_ID}/services",
)
j = r.json()
assert len(j) == 1, r.text

###

###  Test client availability
r = requests.post(
    localhost + f"client_weekly_slot/{CLIENT_ID}",
    headers=headers,
    json={
        "mo": [["13:15", "14:00"], ["15:00", "23:00"]],
        "tu": None,
        "we": None,
        "th": None,
        "fr": None,
        "st": None,
        "su": None,
    },
)
assert r.status_code == 200, r.text

# r = requests.get(
#     localhost + f"client_availability/{CLIENT_ID}",
#     headers=headers,
# )
# days = r.json()["days"]
# for day in days:
#     date = day["date"]
#     date = datetime.datetime.fromisoformat(date)
#     if date.weekday() == 0:
#         break

# assert date.weekday() == 0
# timeslots = day["timeslots"]
# assert timeslots[0]["dt_from"] == "2021-11-29T13:15:00"
# assert timeslots[0]["dt_to"] == "2021-11-29T14:00:00"
# assert timeslots[1]["dt_from"] == "2021-11-29T15:00:00"
# assert timeslots[1]["dt_to"] == "2021-11-29T15:45:00"
# print(timeslots)
###


### Test worker availability
r = requests.get(
    localhost + f"worker_availability/{WORKER_ID}?service_id={SERVICE_ID}",
    headers=headers,
)
assert r.status_code == 200, r.text

days = r.json()["days"]
for day in days:
    date = day["date"]
    date = datetime.datetime.fromisoformat(date)
    if date.weekday() == 0:
        break

assert date.weekday() == 0
timeslots = day["timeslots"]
assert timeslots[0]["dt_from"] == "2021-12-06T13:15:00"
assert timeslots[0]["dt_to"] == "2021-12-06T14:00:00"
assert timeslots[1]["dt_from"] == "2021-12-06T15:00:00"
assert timeslots[1]["dt_to"] == "2021-12-06T15:45:00"
# print(timeslots)

## WORKER_NO_SCHEDULE_ID
r = requests.post(
    localhost + f"slot",
    headers=headers,
    json={
        "name": "Рабочее время",
        "slot_type": "available",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "from_datetime": "2022-01-01T08:00:00",
        "to_datetime": "2022-01-01T18:00:00",
    },
)
assert r.status_code == 200, r.text

r = requests.post(
    localhost + f"public_slot",
    json={
        "name": "Визит клиент",
        "slot_type": "visit",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "from_datetime": "2022-01-01T09:00:00",
        "to_datetime": "2022-01-01T10:00:00",
    },
)
assert r.status_code == 200, r.text

r = requests.get(
    localhost + f"worker_availability/{WORKER_NO_SCHEDULE_ID}",
    headers=headers,
)

days = r.json()["days"]
# print(days)
assert len(days) == 1
day = days[0]
assert len(day["timeslots"]) == 2, day[
    "timeslots"
]  # assert 2 timeslots, no split by time requested

r = requests.post(
    localhost + f"slot",
    headers=headers,
    json={
        "name": "Визит клиент",
        "slot_type": "visit",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "from_datetime": "2022-01-01T09:45:00",
        "to_datetime": "2022-01-01T10:00:00",
    },
)

assert r.status_code == 409, r.text

##


# r = requests.post(
#     localhost + "worker_weekly_slot/1",
#     headers=headers,
#     json={
#         "mo": [["03:01:01", "05:01:01"]],
#         "tu": None,
#         "we": None,
#         "th": None,
#         "fr": None,
#         "st": None,
#         "su": None,
#     },
# )
# print(r.text)

print("*" * 20)
print(" " * 5, "SUCCESS")
print("*" * 20)
