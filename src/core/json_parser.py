#/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Copyright (C) 2017-2018 Artyom Bulgakov

This file is part of viklund.
Viklund is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
Viklund is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with viklund.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
import viklund

class JsonParser():
	@staticmethod
	def parse_import(json_data):
		"""
		Parse import config and return it as dictionary (see example.json)
		
		Parameters
		----------
		json_data
			Opened .json file object.
		section
			Section of JSON.
		Returns
		-------
			commands : dict
				Dictionary with call_command as key and import_id as value.
		"""
		commands = {}
		for items in json_data['import']:
			j_key = items['call_command']
			j_value = items['import_id']
			commands[j_key] = j_value
		return commands

	@staticmethod
	def read_json(path_to_file):
		"""
		Read .json import config file.

		Parameters
		----------
		path_to_file : string
			Path to file.

		Returns
			json_data
				Opened .json import config file object.
		_______
			commands : dict
				Dictionary with call_command as key and import_id as value.
		"""
		with open(path_to_file) as json_file:
			json_data = json.load(json_file)
		return json_data