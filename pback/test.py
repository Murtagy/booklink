import datetime
import random

from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

localhost = "http://127.0.0.1:8000/"

### Actions code


def signup(username):
    r = client.post(
        localhost + "signup",
        json={
            "company": "Comp",
            "username": username,
            "password": "123",
            "email": str(random.randint(0, 1000)) + "example@example12.com",
        },
    )
    return r


def login(username):
    r = client.post(
        localhost + "token",
        data={
            "username": username,
            "password": "123",
        },
    )
    return r


def create_worker(*, use_company_schedule=None):
    person = {"name": "Макс", "job_title": "Разработчик"}
    if use_company_schedule is not None:
        person["use_company_schedule"] = use_company_schedule

    r = client.post(
        localhost + "worker",
        headers=headers,
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
        json={"services": selected_services},
        headers=headers,
    )


def get_client_service(client_id):
    return client.get(
        localhost + f"client/{client_id}/services",
    )


def create_client_weekly_slot(client_id, schedule):
    return client.post(
        localhost + f"client/{client_id}/client_weekly_slot",
        headers=headers,
        json=schedule,
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


def create_visit_as_a_client(slot):
    url = localhost + f"visit"

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


def get_me():
    return client.get(localhost + "users/me", headers=headers)


### Tests code


def test_portyanka():
    global headers

    ### CREATE NEW CLIENT
    username = (
        str(random.randint(0, 1000))
        + str(random.randint(0, 1000))
        + str(random.randint(0, 1000))
        + "test2"
    )
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
    r = create_worker()
    # print(r.text)

    r = get_workers()
    # print(r.text)
    assert len(r.json()) == 1, r.text
    WORKER_ID = r.json()["workers"][0]["worker_id"]
    ###

    ### Create worker (2)
    r = create_worker(use_company_schedule=True)
    # assert r.status_code == 428

    ### Create worker (3)
    r = create_worker(use_company_schedule=False)
    # print(r.text)
    WORKER_NO_SCHEDULE_ID = r.json()["worker_id"]

    ### Check workers n
    r = get_workers()
    # print(r.text)
    assert len(r.json()["workers"]) == 3
    ###

    ### Services
    r = create_service(
        {
            "name": "Стрижка",
            "price": 13.1,
            # price_lower_bound: Optional[float]
            # price_higher_bound: Optional[float]
            "seconds": 45 * 60,
            "description": "Ножницы, все такое",
        }
    )

    SERVICE_ID = r.json()["service_id"]

    r = get_service(SERVICE_ID)
    assert r.json()["service_id"] == SERVICE_ID, r.text

    r = create_service(
        {
            "name": "Стрижка",
            "price": 13.1,
            # price_lower_bound: Optional[float]
            # price_higher_bound: Optional[float]
            "seconds": 45 * 60,
            "description": "Ножницы, все такое",
        }
    )

    SERVICE_ID2 = r.json()["service_id"]
    r = get_client_service(CLIENT_ID)
    j = r.json()
    assert len(j) == 1, r.text

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

    r = create_client_weekly_slot(CLIENT_ID, schedule)
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
    dt_from0, dt_to0 = parse(timeslots[0]["dt_from"]), parse(timeslots[0]["dt_to"])
    dt_from1, dt_to1 = parse(timeslots[1]["dt_from"]), parse(timeslots[1]["dt_to"])
    assert (dt_to0 - dt_from0).total_seconds() / 60 == 45
    assert (dt_to1 - dt_from1).total_seconds() / 60 == 45
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
    dt_from0, dt_to0 = parse(timeslots[0]["dt_from"]), parse(timeslots[0]["dt_to"])
    dt_from1, dt_to1 = parse(timeslots[1]["dt_from"]), parse(timeslots[1]["dt_to"])
    assert (dt_to0 - dt_from0).total_seconds() / 60 == 90
    assert (dt_to1 - dt_from1).total_seconds() / 60 == 90

    ## WORKER_NO_SCHEDULE_ID
    slot = {
        "name": "Рабочее время",
        "slot_type": "available",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "from_datetime": "2022-01-01T08:00:00",
        "to_datetime": "2022-01-01T18:00:00",
    }
    r = create_slot(slot)

    assert r.status_code == 200, r.text

    visit = {
        "name": "Визит клиент",
        "slot_type": "visit",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "from_datetime": "2022-01-01T09:00:00",
        "to_datetime": "2022-01-01T10:00:00",
    }
    r = create_visit_as_a_client(visit)

    assert r.status_code == 200, r.text

    r = get_worker_availability(CLIENT_ID, WORKER_NO_SCHEDULE_ID)

    days = r.json()["days"]
    # print(days)
    assert len(days) == 1
    day = days[0]
    assert len(day["timeslots"]) == 2, day[
        "timeslots"
    ]  # assert 2 timeslots, no split by time requested

    visit = {
        "name": "Визит клиент",
        "slot_type": "visit",
        "client_id": CLIENT_ID,
        "worker_id": WORKER_NO_SCHEDULE_ID,
        "from_datetime": "2022-01-01T09:45:00",
        "to_datetime": "2022-01-01T10:00:00",
    }

    r = create_visit_as_a_client(visit)
    assert r.status_code == 409, r.text

    ##

    # r = client.post(
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
