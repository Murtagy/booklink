import datetime
import random

from fastapi.testclient import TestClient

from .apps.app import app

client = TestClient(app)

localhost = "http://127.0.0.1:8000/"
tmrw = datetime.date.today() + datetime.timedelta(days=1)
username = f"nn{random.randint(0, 100000000)}"
username = "nn"
### Actions code


def signup(username):
    r = client.post(
        localhost + "signup",
        json={
            "company": "Comp",
            "username": username,
            "password": "nn",
            "email": str(random.randint(0, 1000)) + "example@example12.com",
        },
    )
    return r


def login(username):
    r = client.post(
        localhost + "token",
        data={
            "username": username,
            "password": "nn",
        },
    )
    return r


def create_worker(name: str):
    person = {"name": name, "job_title": "машиноместо"}

    r = client.post(
        localhost + "worker",
        headers=headers,  # type: ignore[name-defined]
        json=person,
    )
    return r


def get_workers():
    r = client.get(
        localhost + "workers",
        headers=headers,
    )
    return r


def create_service(service):
    r = client.post(
        localhost + f"service",
        headers=headers,
        json=service,
    )
    return r


def update_service(service, service_id):
    r = client.post(
        localhost + f"service/{service_id}",
        headers=headers,
        json=service,
    )
    return r


def get_service(service_id):
    return client.get(
        localhost + f"service/{service_id}",
    )


def add_worker_skill(worker_id, service_ids):
    selected_services = []
    for s in service_ids:
        selected_services.append({"worker_id": worker_id, "service_id": s, "picked": True})
    return client.post(
        localhost + "worker_services",
        json={"skills": selected_services},
        headers=headers,
    )


def get_client_service(client_id):
    return client.get(
        localhost + f"client/{client_id}/services",
    )


def create_worker_weekly_slot(worker_id, schedule):
    days = []
    for weekday_i, (weekday_str, timeslots) in enumerate(schedule.items()):
        for i in range(90):
            date = tmrw + datetime.timedelta(days=i)
            if date.weekday() == weekday_i:
                if not timeslots:
                    continue
                slots = []
                for t in timeslots:
                    _from_h, _from_m = map(int, t[0].split(":"))
                    _to_h, _to_m = map(int, t[1].split(":"))
                    _from = datetime.datetime(
                        year=date.year,
                        month=date.month,
                        day=date.day,
                        hour=_from_h,
                        minute=_from_m,
                    )
                    _to = datetime.datetime(
                        year=date.year,
                        month=date.month,
                        day=date.day,
                        hour=_to_h,
                        minute=_to_m,
                    )
                    slots.append(
                        {
                            "from_datetime": _from.isoformat(),
                            "to_datetime": _to.isoformat(),
                            "slot_type": "available",
                        }
                    )
                day = {
                    "date": str(date),
                    "timeslots": slots,
                }
                days.append(day)

    return client.post(
        localhost + f"worker/{worker_id}/availability",
        headers=headers,
        json={"days": days},
    )


def get_worker_availability(client_id, worker_id, services=None):
    url = f"client/{client_id}/worker/{worker_id}/availability"
    if services is not None:
        url += f"?services={','.join([str(i) for i in services])}"
    print(url)

    return client.get(
        url,
        headers=headers,
    )


def create_slot(slot):
    url = localhost + f"slot"

    return client.post(
        url,
        headers=headers,
        json=slot,
    )


def create_visit(slot):
    url = localhost + f"slot" + "?force=false"

    return client.post(
        url,
        headers=headers,
        json=slot,
    )


def create_visit_as_a_customer(slot):
    url = localhost + f"public/visit"

    return client.post(
        url,
        headers=headers,
        json=slot,
    )


def get_visits_days(_from, _to):
    url = localhost + f"visits/by_days"
    return client.post(url, headers=headers, json={"date_from": str(_from), "date_to": str(_to)})


def get_all_slots(_from, _to):
    url = localhost + f"workers_calendar"
    return client.get(
        url,
        headers=headers,
        params={"_from": _from.isoformat(), "_to": _to.isoformat()},
    )


def get_me():
    return client.get(localhost + "users/me", headers=headers)


### Tests code


def test_portyanka():
    global headers

    ### CREATE NEW CLIENT
    r = signup(username)
    assert r.status_code == 200, r.text
    signup_json = r.json()
    # print(r.text)
    CLIENT_ID, token = signup_json["client_id"], signup_json["access_token"]
    AUTH = {"Authorization": "Bearer " + token}
    headers = AUTH
    ###

    ### ASSURE LOGIN
    r = get_me()
    assert r.status_code == 200, r.text

    r = login(username)
    # print(r.text)
    assert r.status_code == 200, r.text
    ###

    ### Create worker
    r = create_worker("Машиноместо 1")
    r = create_worker("Машиноместо 2")
    r = create_worker("Машиноместо 3")

    r = get_workers()
    assert len(r.json()["workers"]) == 3, r.text
    WORKER_ID = r.json()["workers"][0]["worker_id"]
    WORKER_ID2 = r.json()["workers"][1]["worker_id"]
    WORKER_NO_SCHEDULE_ID = r.json()["workers"][2]["worker_id"]

    ### Check workers n
    r = get_workers()
    # print(r.text)
    assert len(r.json()["workers"]) == 3
    ###

    ### Services
    r = create_service(
        {
            "name": "Шиномонтажные работы 1-2 колеса",
            "price": 13.1,
            "minutes": 45,
            "description": "Шины, все такое",
        }
    )

    SERVICE_ID = r.json()["service_id"]

    r = get_service(SERVICE_ID)
    assert r.json()["service_id"] == SERVICE_ID, r.text

    r = create_service(
        {
            "name": "Шиномонтажные работы 1-3 колеса",
            "price": 13.1,
            "minutes": 45,
            "description": "Шины, все такое",
        }
    )

    SERVICE_ID2 = r.json()["service_id"]
    r = get_client_service(CLIENT_ID)
    j = r.json()
    assert len(j) == 1, r.text

    r = update_service(
        {
            "name": "Шиномонтажные работы 1-4 колеса",
            "price": 13.1,
            "minutes": 45,
            "description": "Шиины, все такое",
        },
        SERVICE_ID2,
    )
    r = get_service(SERVICE_ID2)
    assert r.json()["name"] == "Шиномонтажные работы 1-4 колеса", r.text

    ###

    ###  Test client availability
    schedule = {
        "mo": [["13:15", "14:00"], ["15:00", "23:00"]],
        "tu": None,
        "we": None,
        "th": None,
        "fr": None,
        "st": None,
        "su": None,
    }

    r = create_worker_weekly_slot(WORKER_ID, schedule)
    assert r.status_code == 200, r.text
    r = create_worker_weekly_slot(WORKER_ID2, schedule)
    assert r.status_code == 200, r.text

    r = client.get(
        localhost + f"client/{CLIENT_ID}/availability/",
        headers=headers,
    )
    availability = r.json()["availability"]

    for days_holder in availability:
        for day in days_holder["days"]:
            date = day["date"]
            date = datetime.datetime.fromisoformat(date)
            if date.weekday() != 0:
                raise ValueError("doesn't start from Monday!")

    ### Test worker availability
    r = get_worker_availability(CLIENT_ID, WORKER_ID, [SERVICE_ID])
    assert r.json() == {"detail": "Worker not skilled of a service"}

    r = add_worker_skill(WORKER_ID, [SERVICE_ID, SERVICE_ID2])
    assert r.status_code == 200, r.text

    r = get_worker_availability(CLIENT_ID, WORKER_ID, [SERVICE_ID])
    assert r.status_code == 200, r.text

    days = r.json()["days"]
    for day in days:
        date = day["date"]
        date = datetime.datetime.fromisoformat(date)
        if date.weekday() != 0:
            raise ValueError("doesn't start from Monday!")

    timeslots = day["timeslots"]

    parse = datetime.datetime.fromisoformat
    from_datetime0, to_datetime0 = parse(timeslots[0]["from_datetime"]), parse(
        timeslots[0]["to_datetime"]
    )
    from_datetime1, to_datetime1 = parse(timeslots[1]["from_datetime"]), parse(
        timeslots[1]["to_datetime"]
    )
    assert (to_datetime0 - from_datetime0).total_seconds() / 60 == 45
    assert (to_datetime1 - from_datetime1).total_seconds() / 60 == 45
    # availability for 2 services
    r = get_worker_availability(CLIENT_ID, WORKER_ID, [SERVICE_ID, SERVICE_ID2])
    assert r.status_code == 200, r.text
    # print(r.text)

    days = r.json()["days"]
    for day in days:
        date = day["date"]
        date = datetime.datetime.fromisoformat(date)
        if date.weekday() == 0:
            break

    assert date.weekday() == 0
    timeslots = day["timeslots"]

    parse = datetime.datetime.fromisoformat
    from_datetime0, to_datetime0 = parse(timeslots[0]["from_datetime"]), parse(
        timeslots[0]["to_datetime"]
    )
    from_datetime1, to_datetime1 = parse(timeslots[1]["from_datetime"]), parse(
        timeslots[1]["to_datetime"]
    )
    assert (to_datetime0 - from_datetime0).total_seconds() / 60 == 90
    assert (to_datetime1 - from_datetime1).total_seconds() / 60 == 90

    ## WORKER_NO_SCHEDULE_ID
    slot = {
        "name": "Рабочее время",
        "slot_type": "available",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "from_datetime": f"{tmrw}T08:00:00",
        "to_datetime": f"{tmrw}T18:00:00",
    }
    r = create_slot(slot)

    assert r.status_code == 200, r.text

    visit = {
        "name": "Визит клиент",
        "slot_type": "visit",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "from_datetime": f"{tmrw}T09:00:00",
        "to_datetime": f"{tmrw}T10:00:00",
    }
    r = create_visit(visit)

    assert r.status_code == 200, r.text

    r = get_worker_availability(CLIENT_ID, WORKER_NO_SCHEDULE_ID)
    assert r.status_code == 200, r.text
    day = [d for d in r.json()["days"] if d["date"] == str(tmrw)][0]
    assert len(day["timeslots"]) == 2, day[
        "timeslots"
    ]  # assert 2 timeslots, no split by time requested

    visit = {
        "name": "Визит клиент",
        "slot_type": "visit",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "from_datetime": f"{tmrw}T09:45:00",
        "to_datetime": f"{tmrw}T10:00:00",
    }

    r = create_visit(visit)
    assert r.status_code == 409, r.text

    r = get_visits_days(tmrw, tmrw)
    assert r.status_code == 200, r.text
    day = [d for d in r.json()["days"] if d["date"] == str(tmrw)][0]
    visit_details = {
        "email": "example@example.com",
        "phone": 123,
        "first_name": "f",
        "last_name": "l",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "remind_me": False,
        "from_dt": f"{tmrw}T10:30:00",
        "services": [{"service_id": SERVICE_ID}],
    }
    r = create_visit_as_a_customer(visit_details)
    assert r.status_code == 200, r.text

    r = get_all_slots(datetime.date.today(), tmrw)
    assert r.status_code == 200, r.text
    assert len(r.json()["days"]) == 4
    assert r.json()["days"][0]["date"] == str(tmrw)
