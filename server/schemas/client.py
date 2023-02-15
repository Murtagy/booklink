from pydantic import BaseModel as BM


class InClient(BM):
    name: str
    logo: str


class OutClient(InClient):
    name: str
    balance: float
