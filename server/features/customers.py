from pydantic import BaseModel as BM


class CustomerInfoIn(BM):
    # beaty name - person name
    # car name - car code?
    first_name: str | None
    last_name: str | None
    email: str | None
    phone: str | None


class CustomerAtVisit(BM):
    customer_id: int | None
    info: CustomerInfoIn | None
