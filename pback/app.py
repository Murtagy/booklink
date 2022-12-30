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
    workers,
)

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

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SQLModel.metadata.create_all(db.engine)
logger = structlog.get_logger()


class StrEnum(str, Enum):
    ...


@app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}


# USERS
app.post("/signup", response_model=users.TokenOut)(users.create_user_endpoint)
app.get("/users/me/", response_model=users.UserOut)(users.read_users_me_endpoint)
app.get("/my_user", response_model=users.UserOut)(users.read_users_me2_endpoint)
app.post("/token")(users.login_for_access_token_endpoint)


# WORKERS
app.get("/worker/{worker_id}", response_model=workers.OutWorker)(
    workers.get_worker_endpoint
)
app.put("/worker/{worker_id}", response_model=workers.OutWorker)(
    workers.update_worker_endpoint
)
app.delete("/worker/{worker_id}")(workers.delete_worker_endpoint)
app.get("/client/{client_id}/workers", response_model=workers.OutWorkers)(
    workers.get_workers_by_client_endpoint
)
app.get("/workers", response_model=workers.OutWorkers)(workers.get_workers_endpoint)
app.post("/worker", response_model=workers.OutWorker)(workers.create_worker_endpoint)


# SERVICES
app.post("/service", response_model=services.OutService)(
    services.create_service_endpoint
)
app.post("/my_service", response_model=services.OutService)(
    services.my_create_service_endpoint
)
app.get("/service/{service_id}", response_model=services.OutService)(
    services.get_service_endpoint
)
app.get("/client/{client_id}/service/{service_id}", response_model=services.OutService)(
    services.get_service_by_client_endpoint
)
app.get("/client/{client_id}/services", response_model=services.OutServices)(
    services.get_services_by_client_endpoint
)

# WORKER-SERVICE
app.post("/worker_services", response_model=skills.Received)(skills.add_skills_endpoint)
app.post("/worker_service", response_model=skills.Received)(skills.add_skill_endpoint)

app.post("/my_worker_services", response_model=skills.Received)(skills.my_add_skill)
app.get("/client/{client_id}/picker/services", response_model=skills.SkillsOut)(
    skills.get_skills_endpoint
)


# SLOTS
app.post("/slot", response_model=slots.Slot)(visits.create_slot_endpoint)
app.delete("/slot/{slot_id}", response_model=slots.Slot)(
    slots.delete_client_slot_endpoint
)
app.post("/client/{client_id}/client_weekly_slot")(
    slots.create_client_weekly_slot_endpoint
)
app.post("/worker_weekly_slot/{worker_id}")(slots.create_worker_weekly_slot_endpoint)


# VISITS
app.get("/visit/{visit_id}", response_model=visits.OutVisit)(visits.get_visit_endpoint)
app.get("/visits")(visits.get_visits_endpoint)
app.post("/visit", response_model=visits.OutVisit)(visits.create_visit_slot_endpoint)
app.post("/public/visit", response_model=visits.OutVisit)(
    visits.public_book_visit_endpoint
)
app.put("/visit/{visit_id}")(visits.update_visit_endpoint)


# AVAILABILITY
app.get(
    "/client/{client_id}/worker/{worker_id}/availability",
    response_model=availability.Availability,
)(availability.get_worker_availability_endpoint)
app.get(
    "/client/{client_id}/availability/",
    response_model=availability.AvailabilityPerWorker,
)(availability.get_client_availability_endpoint)


# FILES
app.post("/file")(files.create_file_endpoint)
app.get("/file/{file_name}")(files.get_file_endpoint)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
