import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from ..features import availability, services, skills, slots, workers

# docs_kwargs = {}
# if settings.ENVIRONMENT == 'production':
# if False:
# docs_kwargs = dict(docs_url=None, redoc_url=None)

# app = FastAPI(**docs_kwargs)
ORIGINS = [
    "http://127.0.0.1:5173",
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
logger = structlog.get_logger()


@app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}


# WORKERS
app.get("/worker/{worker_id}", response_model=workers.OutWorker)(workers.get_worker)
app.get("/client/{client_id}/workers", response_model=workers.OutWorkers)(
    workers.get_workers_by_client
)
app.get("/workers", response_model=workers.OutWorkers)(workers.get_workers)


# SERVICES
app.get("/service/{service_id}", response_model=services.OutService)(services.get_service)
app.get("/client/{client_id}/service/{service_id}", response_model=services.OutService)(
    services.get_service_by_client
)
app.get("/client/{client_id}/services", response_model=services.OutServices)(
    services.get_services_by_client
)

# WORKER-SERVICE
app.get("/client/{client_id}/picker/services", response_model=skills.SkillsOut)(workers.get_skills)


# VISITS
app.get("/visit/{visit_id}", response_model=slots.OutVisit)(slots.get_visit)
app.post("/public/visit", response_model=slots.OutVisitExtended)(slots.public_book_visit)


# AVAILABILITY
app.get(
    "/client/{client_id}/worker/{worker_id}/availability",
    response_model=availability.Availability,
)(availability.get_worker_availability)
app.get(
    "/client/{client_id}/availability/",
    response_model=availability.AvailabilityPerWorker,
)(availability.get_client_availability)
