from enum import Enum

import structlog
import uvicorn  # type: ignore
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

import db
from features import (
    availability,
    files,
    services,
    skills,
    slots,
    users,
    visits,
)
from features.workers import schemas as workers_schemas
from features.workers import api as workers_api
from fastapi.routing import APIRoute

# docs_kwargs = {}
# if settings.ENVIRONMENT == 'production':
# if False:
# docs_kwargs = dict(docs_url=None, redoc_url=None)

# app = FastAPI(**docs_kwargs)
ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:3333",
    "http://localhost:3000",
]

def custom_generate_unique_id(route: APIRoute):
    # https://fastapi.tiangolo.com/nl/advanced/generate-clients/#custom-generate-unique-id-function
    # function name and method is enough IMO
    return f"{route.name}"


app = FastAPI(generate_unique_id_function=custom_generate_unique_id)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SQLModel.metadata.create_all(db.engine)
logger = structlog.get_logger()




@app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}


# USERS
app.post("/signup", response_model=users.TokenOut)(users.create_user)
app.get("/users/me/", response_model=users.UserOut)(users.read_users_me)
app.get("/my_user", response_model=users.UserOut)(users.read_users_me2)
app.post("/token")(users.login_for_access_token)


# WORKERS
app.get("/worker/{worker_id}", response_model=workers_schemas.OutWorker)(workers_api.get_worker)
app.put("/worker/{worker_id}", response_model=workers_schemas.OutWorker)(workers_api.update_worker)
app.delete("/worker/{worker_id}")(workers_api.delete_worker)
app.get("/client/{client_id}/workers", response_model=workers_schemas.OutWorkers)(
    workers_api.get_workers_by_client
)
app.get("/workers", response_model=workers_schemas.OutWorkers)(workers_api.get_workers)
app.post("/worker", response_model=workers_schemas.OutWorker)(workers_api.create_worker)


# SERVICES
app.post("/service", response_model=services.OutService)(services.create_service)
app.post("/my_service", response_model=services.OutService)(services.my_create_service)
app.get("/service/{service_id}", response_model=services.OutService)(services.get_service)
app.get("/client/{client_id}/service/{service_id}", response_model=services.OutService)(
    services.get_service_by_client
)
app.get("/client/{client_id}/services", response_model=services.OutServices)(
    services.get_services_by_client
)

# WORKER-SERVICE
app.post("/worker_services", response_model=skills.Received)(skills.add_skills)
app.post("/worker_service", response_model=skills.Received)(skills.add_skill)

app.post("/my_worker_services", response_model=skills.Received)(skills.my_add_skill)
app.get("/client/{client_id}/picker/services", response_model=skills.SkillsOut)(
    skills.get_skills
)


# SLOTS
app.post("/slot", response_model=slots.Slot)(visits.create_slot)
app.delete("/slot/{slot_id}", response_model=slots.Slot)(slots.delete_client_slot)
app.post("/client/{client_id}/client_weekly_slot")(slots.create_client_weekly_slot)
app.post("/worker_weekly_slot/{worker_id}")(slots.create_worker_weekly_slot)


# VISITS
app.get("/visit/{visit_id}", response_model=visits.OutVisit)(visits.get_visit)
app.get("/visits")(visits.get_visits)
app.post("/visit", response_model=visits.OutVisit)(visits.create_visit_slot)
app.post("/public/visit", response_model=visits.OutVisit)(visits.public_book_visit)
app.put("/visit/{visit_id}")(visits.update_visit)


# AVAILABILITY
app.get(
    "/client/{client_id}/worker/{worker_id}/availability",
    response_model=availability.Availability,
)(availability.get_worker_availability)
app.get(
    "/client/{client_id}/availability/",
    response_model=availability.AvailabilityPerWorker,
)(availability.get_client_availability)


# FILES
app.post("/file")(files.create_file)
app.get("/file/{file_name}")(files.get_file)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
