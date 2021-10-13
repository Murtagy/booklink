from typing import Optional

from pydantic import BaseModel as BM


class CreateWorker(BM):
    name: str


class UpdateWorker(BM):
    worker_id: int
    name: Optional[str]
    job_title: Optional[str]
    use_company_schedule: Optional[bool]

    display_name: Optional[str]
    display_job_title: Optional[str]
    display_description: Optional[str]
    photo_id: Optional[int]


class OutWorker(BM):
    id: str
    name: str
    display_name: str
    display_job_title: str
    display_description: str
    use_company_schedule: bool
    photo_id: int

    class Config:
        orm_mode = True
