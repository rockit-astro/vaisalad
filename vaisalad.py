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

import datetime
import re
import serial
import threading
import time

class VaisalaDaemon:
    SERIAL_PORT = '/dev/ttyACM0'
    SERIAL_BAUD = 9600
    SERIAL_TIMEOUT = 5

    DATA_REGEX = b'0R0,' \
        b'Dm=(?P<wind_direction>\d+)D,' \
        b'Sm=(?P<wind_speed>\d+\.\d)K,' \
        b'Ta=(?P<temperature>\d+\.\d)C,' \
        b'Ua=(?P<relative_humidity>\d+\.\d)P,' \
        b'Pa=(?P<pressure>\d+\.\d)H,' \
        b'Rc=(?P<accumulated_rain>\d+\.\d\d)M,' \
        b'Th=(?P<heater_temperature>\d+\.\d)C,' \
        b'Vh=(?P<heater_voltage>\d+\.\d)N\r\n'

    def __init__(self):
        self.data_received = datetime.datetime.min
        self.wind_direction = 0
        self.wind_speed = 0
        self.temperature = 0
        self.relative_humidity = 0
        self.pressure = 0
        self.accumulated_rain = 0
        self.heater_temperature = 0
        self.heater_voltage = 0

        self._lock = threading.Lock()
        self._regex = re.compile(VaisalaDaemon.DATA_REGEX)
        self._port = serial.Serial(VaisalaDaemon.SERIAL_PORT,
                                   VaisalaDaemon.SERIAL_BAUD,
                                   timeout=VaisalaDaemon.SERIAL_TIMEOUT)
        
        # Flush any stale state
        self._port.flushInput()
        self._port.flushOutput()

        # First line may have been only partially recieved
        self._port.readline()
        
        runloop = threading.Thread(target=self.run)
        runloop.daemon = True
        runloop.start()

    def run(self):
        while True:
            data = self._port.readline()
            match = self._regex.match(data)

            if match:
                with self._lock:
                    self.data_received = datetime.datetime.utcnow()
                    self.wind_direction = int(match.group('wind_direction'))
                    self.wind_speed = float(match.group('wind_speed'))
                    self.temperature = float(match.group('temperature'))
                    self.relative_humidity = float(match.group('relative_humidity'))
                    self.pressure = float(match.group('pressure'))
                    self.accumulated_rain = float(match.group('accumulated_rain'))
                    self.heater_temperature = float(match.group('heater_temperature'))
                    self.heater_voltage = float(match.group('heater_voltage'))

# TODO: Split this out into a client program
vaisala = VaisalaDaemon()
last_update = datetime.datetime.min
while True:
    time.sleep(.1)
    with vaisala._lock:
        if last_update < vaisala.data_received:
            print('Data received {}:'.format(vaisala.data_received))
            print(u'Wind Direction: {} \u00B0'.format(vaisala.wind_direction))
            print( '    Wind Speed: {} km/h'.format(vaisala.wind_speed))
            print(u'   Temperature: {} \u2103'.format(vaisala.temperature))
            print( ' Rel. Humidity: {} %'.format(vaisala.relative_humidity))
            print( '      Pressure: {} hPa'.format(vaisala.pressure))
            print( '   Accum. Rain: {} mm'.format(vaisala.accumulated_rain))
            print(u'  Heater Temp.: {} \u2103'.format(vaisala.heater_temperature))
            print( 'Heater Voltage: {} V'.format(vaisala.heater_voltage))

            last_update = vaisala.data_received
