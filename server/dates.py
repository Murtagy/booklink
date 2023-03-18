import datetime

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
