from astral import LocationInfo
import datetime
from astral.sun import sun

CITY = LocationInfo("London", "England", "Europe/London", 51.5, -0.116)


def past_sunset():
    now = datetime.datetime.now()
    s = sun(CITY.observer, date=now)
    sunset = s["sunset"]

    # Convert sunset to datetime so it is comparable to now
    sunset = datetime.datetime(day=sunset.day,
                               month=sunset.month,
                               year=sunset.year,
                               hour=sunset.hour,
                               minute=sunset.minute,
                               second=sunset.second)
    if sunset < now:
        return True
    else:
        return False
