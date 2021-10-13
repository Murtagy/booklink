from pydantic import BaseModel as BM


class InWorker(BM):
    id: str
    name: str
    job_title: str
    use_company_schedule: bool


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
