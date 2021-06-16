#!/usr/bin/python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime as dt, timezone, timedelta
from enum import Enum
import requests
import subprocess
import sys
import time

LAT = '38.8462'
LNG = '-77.3064'
NIGHT_TEMP = 2500


def main():
    last = None
    while True:
        next_mode = get_next(last)
        if next_mode != last:
            switch_mode(next_mode)
            last = next_mode
        time.sleep(300)


@dataclass
class SunSchedule:
    sunrise: time
    sunset: time


class Period(Enum):
    DAY = 'day'
    NIGHT = 'night'


def get_next(last: Period):
    sched = get_schedule()
    now = dt.now().time()
    if sched.sunrise < now < sched.sunset and last != Period.DAY:
        return Period.DAY
    elif sched.sunrise > now or now > sched.sunset and last != Period.NIGHT:
        return Period.NIGHT
    else:
        return last


def switch_mode(mode: Period):
    {
        Period.NIGHT: set_night,
        Period.DAY: set_day
    }[mode]()


def get_schedule() -> SunSchedule:
    url = f'https://api.sunrise-sunset.org/json?lat={LAT}&lng={LNG}&date=today'
    response = requests.get(url).json()
    return SunSchedule(
        parse_utc_to_local(response['results']['sunrise'], '%I:%M:%S %p'),
        parse_utc_to_local(response['results']['sunset'], '%I:%M:%S %p'),
    )


def parse_utc_to_local(utc_timestamp: str, pattern: str):
    return dt.strptime(utc_timestamp, pattern)\
        .replace(tzinfo=timezone.utc)\
        .astimezone(current_timezone())\
        .time()


def current_timezone():
    if time.daylight:
        return timezone(timedelta(seconds=-time.altzone),time.tzname[1])
    else:
        return timezone(timedelta(seconds=-time.timezone),time.tzname[0])


def set_night():
    log('goodnight! setting to night mode.')
    set_brightness(0)
    set_color_temperature(NIGHT_TEMP)
    log('night mode enabled.')


def set_day():
    log('good morning! setting to day mode.')
    set_brightness(100)
    set_color_temperature(None)
    log('day mode enabled.')


def set_brightness(brightness: int):
    subprocess.run(['ddccontrol', '-p', '-r', '0x10', '-w', str(brightness)])


def set_color_temperature(temp: int):
    if temp == None:
        subprocess.run(['redshift', '-x'])
    else:
        subprocess.run(['redshift', '-PO', str(temp)])


def log(*msg):
    print(*msg)
    sys.stdout.flush()


if __name__ == '__main__':
    main()