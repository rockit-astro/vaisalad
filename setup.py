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

import distutils.core
import os

README_PATH = os.path.join(os.getcwd(), 'README.md')

# rpmbuild mangles the absolute path, so try a fallback
if not os.path.exists(README_PATH):
    README_PATH = os.path.join(os.getcwd(), '../../../../../README.md')

distutils.core.setup(name='onemetre-vaisalad',
    version='1.0',
    author="Paul Chote",
    author_email="p.chote@warwick.ac.uk",
    url="https://github.com/warwick-one-metre/vaisalad",
    description="Weather station daemon for the Warwick one-metre telescope.",
    long_description=open(README_PATH).read(),
    license="GPL3",

    options = {'bdist_rpm': {
      'post_install' : 'postinstall.sh',
      'group' : 'Unspecified',
      'requires' : 'python3'
    }},

    scripts=['vaisalad', 'vaisala'],
    data_files=[
        ('/usr/lib/udev/rules.d', ['10-onemetre-vaisala.rules']),
        ('/usr/lib/systemd/system', ['vaisalad.service']),
    ],
)
