from pydantic import BaseModel as BM


class InWorker(BM):
    id: str
    name: str
    job_title: str
    use_company_working_hours: bool
    # photo?


class OutWorker(BM):
    id: str
    name: str
    job_title: str


# TODO: расписания для сотрудников
