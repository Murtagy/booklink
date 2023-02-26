from pydantic import BaseModel as BM
from sqlalchemy.orm import Session  # type: ignore

from .. import crud
from . import services


class SkillOut(BM):
    picked: bool
    service: services.OutService


class SkillsOut(BM):
    skills: list[SkillOut]


def get_worker_skills_including_not_picked(
    s: Session, client_id: int, worker_id: int | None
) -> SkillsOut:
    skills_out: list[SkillOut] = []
    client_services = services.get_services(client_id, s=s)
    worker_services = services.get_services(client_id, worker_id, s)

    for cs in client_services.services:
        worker_picked_service = cs in worker_services.services
        service_out = SkillOut(picked=worker_picked_service, service=cs)
        skills_out.append(service_out)

    return SkillsOut(skills=skills_out)


def create_skill(s: Session, worker_id: int, service_id: int) -> None:
    crud.create_skill(s, worker_id, service_id)
