from pydantic import BaseModel as BM


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


class OutWorkers(BM):
    workers: list[OutWorker]
