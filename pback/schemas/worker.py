
from pydantic import BaseModel as BM

class InWorker(BM):
    id: str
    name: str
    job_title: str
    use_company_working_hours: bool
    # specific_working_hours: List[Tuple]
    # photo?

class OutWorker(BM):
    id: str
    name: str
    job_title: str



