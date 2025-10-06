""" 
gw4xxx-hal - IoTmaxx Gateway Hardware Abstraction Layer
Copyright (C) 2021-2025 IoTmaxx GmbH

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import gpiod

gpiod_v2 = hasattr(gpiod, "api_version")

if gpiod_v2:
    from .libgpiod2_wrapper import Libgpiod2Wrapper
    libgpiod = Libgpiod2Wrapper()
else:
    from .libgpiod1_wrapper import Libgpiod1Wrapper
    libgpiod = Libgpiod1Wrapper()
