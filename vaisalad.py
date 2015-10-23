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

"""Daemon process for managing a Vaisala WXT520 weather station via RS232"""

import datetime
import Pyro4
import re
import serial
import threading

PYRO_HOST = 'localhost'
PYRO_PORT = 9001

class VaisalaDaemon:
    """Daemon class that wraps the RS232 interface"""
    SERIAL_PORT = '/dev/ttyACM0'
    SERIAL_BAUD = 9600
    SERIAL_TIMEOUT = 5

    # pylint: disable=anomalous-backslash-in-string
    DATA_REGEX = b'0R0,' \
        b'Dm=(?P<wind_direction>\d+)D,' \
        b'Sm=(?P<wind_speed>\d+\.\d)K,' \
        b'Ta=(?P<temperature>\d+\.\d)C,' \
        b'Ua=(?P<relative_humidity>\d+\.\d)P,' \
        b'Pa=(?P<pressure>\d+\.\d)H,' \
        b'Rc=(?P<accumulated_rain>\d+\.\d\d)M,' \
        b'Th=(?P<heater_temperature>\d+\.\d)C,' \
        b'Vh=(?P<heater_voltage>\d+\.\d)N\r\n'
    # pylint: enable=anomalous-backslash-in-string

    def __init__(self):
        self._lock = threading.Lock()
        self._running = True
        self._regex = re.compile(VaisalaDaemon.DATA_REGEX)
        self._port = serial.Serial(VaisalaDaemon.SERIAL_PORT,
                                   VaisalaDaemon.SERIAL_BAUD,
                                   timeout=VaisalaDaemon.SERIAL_TIMEOUT)

        self._latest = None

        # Flush any stale state
        self._port.flushInput()
        self._port.flushOutput()

        # First line may have been only partially recieved
        self._port.readline()

        runloop = threading.Thread(target=self.run)
        runloop.daemon = True
        runloop.start()

    def run(self):
        """Main run loop"""
        while self._running:
            data = self._port.readline()
            match = self._regex.match(data)

            if match:
                with self._lock:
                    self._latest = {k: float(v) for k, v
                                    in match.groupdict().items()}
                    self._latest['date'] = datetime.datetime.utcnow()

    def running(self):
        """Returns false if the daemon should be terminated"""
        return self._running

    def stop(self):
        """Stop the daemon thread"""
        self._running = False

    def latest_measurement(self):
        """Query the latest valid measurement.  May return None if no data
        is available"""
        with self._lock:
            return self._latest

def spawn_daemon():
    """Spawns the daemon and registers it with Pyro"""
    Pyro4.config.COMMTIMEOUT = 5

    pyro = Pyro4.Daemon(host=PYRO_HOST, port=PYRO_PORT)
    vaisala = VaisalaDaemon()
    uri = pyro.register(vaisala, objectId='vaisala_daemon')

    print('Starting vaisala daemon with Pyro ID:', uri)
    pyro.requestLoop(loopCondition=vaisala.running)
    print('Stopping vaisala daemon with Pyro ID:', uri)

if __name__ == '__main__':
    spawn_daemon()
