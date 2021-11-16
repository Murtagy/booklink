from typing import Optional

from pydantic import BaseModel as BM


class CreateWorker(BM):
    name: str
    job_title: str
    use_company_schedule: Optional[bool]


class UpdateWorker(BM):
    # worker_id: int
    name: Optional[str]
    job_title: Optional[str]
    use_company_schedule: Optional[bool]

    display_name: Optional[str]
    display_job_title: Optional[str]
    display_description: Optional[str]
    photo_id: Optional[int]


class OutWorker(BM):
    worker_id: str
    name: str
    job_title: str
    display_name: Optional[str]
    display_job_title: Optional[str]
    display_description: Optional[str]
    use_company_schedule: bool
    photo_id: Optional[int]

    class Config:
        orm_mode = True
