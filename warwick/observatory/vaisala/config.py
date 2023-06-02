#
# This file is part of vaisalad
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

"""Helper function to validate and parse the json config file"""

import json
from warwick.observatory.common import daemons, IP, validation

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['daemon', 'log_name', 'control_machines', 'reset_rain_time'],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'log_name': {
            'type': 'string',
        },
        'control_machines': {
            'type': 'array',
            'items': {
                'type': 'string',
                'machine_name': True
            }
        },
        'reset_rain_time': {
            'type': 'string',
        },
        'serial_port': {
            'type': 'string',
        },
        'serial_baud': {
            'type': 'number',
            'min': 0
        },
        'serial_timeout': {
            'type': 'number',
            'min': 0
        },
        'socket_ip': {
            'type': 'string',
        },
        'socket_port': {
            'type': 'number',
            'min': 0
        },
        'socket_timeout': {
            'type': 'number',
            'min': 0
        }
    },
    'anyOf': [
        {'required': ['serial_port', 'serial_baud', 'serial_timeout']},
        {'required': ['socket_ip', 'socket_port', 'socket_timeout']}
    ]
}


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r', encoding='utf-8') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validation.validate_config(config_json, CONFIG_SCHEMA, {
            'daemon_name': validation.daemon_name_validator
        })

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.control_machines = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.reset_rain_time = config_json['reset_rain_time']
        if 'socket_ip' in config_json:
            self.socket_ip = config_json['socket_ip']
            self.socket_port = int(config_json['socket_port'])
            self.socket_timeout = int(config_json['socket_timeout'])
            self.serial_port = self.serial_baud = self.serial_timeout = None
        else:
            self.serial_port = config_json['serial_port']
            self.serial_baud = int(config_json['serial_baud'])
            self.serial_timeout = int(config_json['serial_timeout'])
            self.socket_ip = self.socket_port = self.socket_timeout = None
