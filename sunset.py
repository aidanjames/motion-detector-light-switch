from astral import LocationInfo
import datetime
from astral.sun import sun

CITY = LocationInfo("London", "England", "Europe/London", 51.5, -0.116)


def past_sunset():
    now = datetime.datetime.now()
    s = sun(CITY.observer, date=now)
    sunset = s["sunset"]

    if sunset.hour > now.hour and sunset.minute > now.minute and now.second > sunset.second:
        return True
    else:
        return False
