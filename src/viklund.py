#Copyright (R) 
#This file is part of viklund.
#
#Viklund is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Viklund is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with viklund.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import
from Vk_random import *
from Vk_exceptions import *
from Vk_group_import import *
from Vk_messages import *
from .system import System
from .logging import Logging

vk = None
vkApi = None
JSON_PATH = None