# Part of the ROBOID project - https://roboticsware.uz
# Copyright (C) 2022 RoboticsWare (neopia.uz@gmail.com)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import sys

class Util(object):
    @staticmethod
    def round(value):
        if isinstance(value, (int, float)):
            if value < 0:
                return -int(0.5 - value)
            else:
                return int(0.5 + value)
        else:
            return 0
    @staticmethod
    def print_message(message):
        sys.stdout.write("{}: {}\n".format('Debug', message))

    @staticmethod
    def print_error(message):
        sys.stderr.write("{}: {}\n".format('Error', message))
