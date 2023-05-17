import datetime
from typing import Any
from pydantic.datetime_parse import parse_datetime

import pytz

timezone = pytz.FixedOffset(60 * 3)  # GTM +3


def localize(d: datetime.datetime):
    if d.tzinfo is None:
        return d
    return d.astimezone(timezone).replace(tzinfo=None)


def date_range(d1: datetime.date, d2: datetime.date) -> list[datetime.date]:
    out = []
    if d2 < d1:
        raise ValueError(f"{d2=}<{d1=}")

    while d2 >= d1:
        out.append(d1)
        d1 = d1 + datetime.timedelta(days=1)
    return out


class LocalisedDatetime(datetime.datetime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any):
        if isinstance(v, datetime.datetime):
            return localize(v)
        try:
            d = parse_datetime(v)
            return localize(d)
        except Exception as e:
            raise ValueError(f'Invalid datetime {v}') from e


# class LocalisedDatetimeBase(BaseModel):
#     class Config:
#         @classmethod
#         def prepare_field(cls, field: ModelField) -> ModelField:
#             if field.annotation == datetime.datetime:
#                 return ModelField.infer(name=field.name, annotation=LocalisedDatetime, class_validators={}, config=BaseConfig)
#             return ModelField.infer(name=field.name, annotation=field.annotation, class_validators={}, config=BaseConfig)
