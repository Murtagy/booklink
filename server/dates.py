import datetime

import pytz

timezone = pytz.FixedOffset(3)


def localize(d: datetime.datetime):
    if d.tzinfo is None:
        return d
    return d.astimezone(timezone).replace(tzinfo=None)
