from pydantic import BaseModel as BM

from features.services import OutService


class CreateWorker(BM):
    name: str
    job_title: str
    use_company_schedule: bool | None


class UpdateWorker(BM):
    # worker_id: int
    name: None | str
    job_title: None | str
    use_company_schedule: None | bool


class OutWorker(BM):
    worker_id: str
    name: str
    job_title: str
    use_company_schedule: bool

    class Config:
        orm_mode = True


class OutWorkers(BM):
    workers: list[OutWorker]


class SkillIn(BM):
    worker_id: int
    service_id: int
    picked: bool = True


class SkillsIn(BM):
    services: list[SkillIn]


class Received(BM):
    msg: str = "Received"
