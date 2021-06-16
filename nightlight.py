#!/usr/bin/python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime as dt
from enum import Enum
from time import sleep
import requests
import subprocess


LAT = '38.8462'
LNG = '-77.3064'
NIGHT_TEMP = 3000


def main():
    last = None
    while True:
        last = update(last)
        sleep(300)


@dataclass
class SunSchedule:
    sunrise: time
    sunset: time


class Period(Enum):
    DAY = 'day'
    NIGHT = 'night'


def update(last: Period):
    sched = get_schedule()
    if sched.sunrise < dt.now().time() < sched.sunset and last != Period.DAY:
        set_day()
        return Period.DAY
    elif last != Period.NIGHT:
        set_night()
        return Period.NIGHT
    else:
        return last


def get_schedule() -> SunSchedule:
    url = f'https://api.sunrise-sunset.org/json?lat={LAT}&lng={LNG}&date=today'
    response = requests.get(url).json()
    return SunSchedule(
        dt.strptime(response['results']['sunrise'], '%I:%M:%S %p').time(),
        dt.strptime(response['results']['sunset'], '%I:%M:%S %p').time(),
    )


def set_night():
    print('goodnight!')
    set_brightness(0)
    set_color_temperature(NIGHT_TEMP)


def set_day():
    print('good morning!')
    set_brightness(100)
    set_color_temperature(None)


def set_brightness(brightness: int):
    subprocess.run(['ddccontrol', '-p', '-r', '0x10', '-w', str(brightness)])


def set_color_temperature(temp: int):
    if temp == None:
        subprocess.run(['redshift', '-x'])
    else:
        subprocess.run(['redshift', '-PO', str(temp)])


if __name__ == '__main__':
    main()