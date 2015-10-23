#!/usr/bin/env python3
#
# This file is part of vaisalad.
#
# vaisalad is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# vaisalad is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with vaisalad.  If not, see <http://www.gnu.org/licenses/>.

"""Commandline client for communicating with vaisalad"""

import Pyro4

DAEMON_URI = 'PYRO:vaisala_daemon@localhost:9001'

def print_latest_measurement():
    """Prints the latest weather data in human-readable form"""
    vaisala = Pyro4.Proxy(DAEMON_URI)
    latest = vaisala.latest_measurement()

    print('Data received {}:'.format(latest['date']))
    print(u'Wind Direction: {} \u00B0'.format(latest['wind_direction']))
    print(u'    Wind Speed: {} km/h'.format(latest['wind_speed']))
    print(u'   Temperature: {} \u2103'.format(latest['temperature']))
    print(u' Rel. Humidity: {} %'.format(latest['relative_humidity']))
    print(u'      Pressure: {} hPa'.format(latest['pressure']))
    print(u'   Accum. Rain: {} mm'.format(latest['accumulated_rain']))
    print(u'  Heater Temp.: {} \u2103'.format(latest['heater_temperature']))
    print(u'Heater Voltage: {} V'.format(latest['heater_voltage']))

if __name__ == '__main__':
    print_latest_measurement()
