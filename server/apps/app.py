import logging

import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from sqlmodel import SQLModel

from .. import db
from ..app_logging import ServerErrorMiddleware, log_request
from ..features import availability, files, services, skills, slots, users, workers
from .public_app import app as public_app

# docs_kwargs = {}
# if settings.ENVIRONMENT == 'production':
# if False:
# docs_kwargs = dict(docs_url=None, redoc_url=None)

# app = FastAPI(**docs_kwargs)
ORIGINS = [
    "http://127.0.0.1:5173",  # localhost
    "http://10.0.0.3:5173",  # over wireguard
    # vpn
    "http://10.20.20.37:5173",
    "http://127.0.0.1",
]


def custom_generate_unique_id(route: APIRoute):
    # https://fastapi.tiangolo.com/nl/advanced/generate-clients/#custom-generate-unique-id-function
    # function name and method is enough IMO
    return f"{route.name}"


# import sentry_sdk
# sentry_sdk.init(
#     dsn="https://c1eba737d6d94d41a730b8dc150fa377@o1278629.ingest.sentry.io/6478409",
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,
#     _experiments={
#         "profiles_sample_rate": 1.0,
#     }
# )

app = FastAPI(generate_unique_id_function=custom_generate_unique_id)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ServerErrorMiddleware, handler=log_request)
SQLModel.metadata.create_all(db.engine)


@app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}


app.mount("/booking_api/", public_app)

# USERS
app.post("/signup", response_model=users.TokenOut)(users.create_user)
app.get("/users/me/", response_model=users.UserOut)(users.read_users_me)
app.get("/my_user", response_model=users.UserOut)(users.read_users_me2)
app.post("/token", response_model=users.TokenOut)(users.login_for_access_token)


# WORKERS
app.get("/worker/{worker_id}", response_model=workers.OutWorker)(workers.get_worker)
app.put("/worker/{worker_id}", response_model=workers.OutWorker)(workers.update_worker)
app.delete("/worker/{worker_id}")(workers.delete_worker)
app.get("/client/{client_id}/workers", response_model=workers.OutWorkers)(
    workers.get_workers_by_client
)
app.get("/workers", response_model=workers.OutWorkers)(workers.get_workers)
app.post("/worker", response_model=workers.OutWorker)(workers.create_worker)


# SERVICES
app.post("/service", response_model=services.OutService)(services.create_service)
app.get("/services", response_model=services.OutServices)(services.get_services_by_user)
app.post("/my_service", response_model=services.OutService)(services.my_create_service)
app.get("/service/{service_id}", response_model=services.OutService)(services.get_service)
app.post("/service/{service_id}", response_model=services.OutService)(services.update_service)
app.delete("/service/{service_id}")(services.delete_service)
app.get("/client/{client_id}/service/{service_id}", response_model=services.OutService)(
    services.get_service_by_client
)
app.get("/client/{client_id}/services", response_model=services.OutServices)(
    services.get_services_by_client
)

# WORKER-SERVICE
app.post("/worker_services", response_model=workers.Received)(workers.add_skills)
app.post("/worker_service", response_model=workers.Received)(workers.add_skill)

app.post("/my_worker_services", response_model=workers.Received)(workers.my_add_skill)
app.get("/skills", response_model=skills.SkillsOut)(workers.get_skills)


# SLOTS
app.post("/slot", response_model=slots.OutSlot)(slots.create_slot_with_check)
app.delete("/slot/{slot_id}", response_model=slots.OutSlot)(slots.delete_client_slot)
app.put("/slot/{slot_id}")(slots.update_slot)
app.put("/slot/{slot_id}/customer")(slots.update_slot_customer_info)
# SLOTS (visits)
app.get("/visit/{visit_id}", response_model=slots.OutVisit)(slots.get_visit)
app.get("/visit_extended/{visit_id}", response_model=slots.OutVisitExtended)(
    slots.get_visit_extended
)
app.get("/visits")(slots.get_visits)
app.post("/visits/by_days", response_model=slots.VisitsByDays)(slots.get_visits_days)
app.get("/workers_calendar", response_model=slots.AllSlots)(slots.workers_calendar)
# tmp:
app.post("/public/visit", response_model=slots.OutVisitExtended)(slots.public_book_visit)

# AVAILABILITY
app.get(
    "/client/{client_id}/worker/{worker_id}/availability",
    response_model=availability.Availability,
)(availability.get_worker_availability)
app.get(
    "/worker/{worker_id}/availability",
    response_model=availability.Availability,
)(availability.get_worker_availability_by_user)
app.get(
    "/client/{client_id}/availability/",
    response_model=availability.AvailabilityPerWorker,
)(availability.get_client_availability)
app.post("/worker/{worker_id}/availability")(availability.create_worker_availability)


# FILES
app.post("/file")(files.create_file)
app.get("/file/{file_name}")(files.get_file)


if __name__ == "__main__":
    # logging.getLogger("uvicorn").handlers.clear()
    uvicorn.run(app, host="0.0.0.0", port=8000)
