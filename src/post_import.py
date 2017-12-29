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

import time
import vk_api
import random
import json
import os
import sys
import getpass
import viklund

class PostImport:
	group_id = None
	posts_count = None
	import_type = None

	@staticmethod
	def get_post(values):
		"""
		Get post from profile or community wall. Wrapper for Vk API's Wall.get() method.
		<https://vk.com/dev/wall.get>
		
		Parameters
		----------
		values : map
			Map with arguments 
		Raises
		-------
			ValueError
				1) If got invalid post_count value.
				2) If got invalie post_offset value.
			vk_api.VkApiError
				VK API errors.
			vk_api.ApiError
				VK API errors.

		"""
		response = None
		try:
			response = viklund.vk.method('wall.get', values)
		except vk_api.VkApiError:
			raise
		except vk_api.ApiError:
			raise
		return response




	def get_request_str(received_str):
		start_index = received_str.find('пост')
		start_index += 4
		request_str = ''
		for i in range(start_index, len(received_str)):
			if received_str[i].isalpha() or received_str[i].isdigit():
				request_str += received_str[i]
		return request_str

	@staticmethod
	def get_import_list(json_data):
		commands = None
		for items in json_data['import']:
			commands += items['call_command'] + '\n'
		return 'Использование: \'/пост <команда>\'\nДоступные команды:\n' + commands
	"""
	@staticmethod
	def handle_import_request(item, received_str):
		path_to_file = viklund.JSON_PATH
		group_import = viklund.Vk_group_import()
		request = group_import.get_request_str(received_str)
		if viklund.Vk_messages.get_dest_type(item):
			chat_id = item[u'chat_id']
		try:
			json_data = group_import.read_json(path_to_file)
			search_result = group_import.search_json(json_data, request)
			if request == '':
				group_import.get_import_list(item, json_data);
				return 0
			if not search_result:
				raise Import_command_not_found_exception()
		except Import_command_not_found_exception:
			viklund.Vk_messages.send_selective(item, 'msg', request + ': запрос не найден')
			return 1
		else:
			group_import.select_and_send_random_group_thing(group_import.get_group_id(), item, group_import.get_import_type()) 
	"""
	def read_json(self, path_to_file):
		with open(path_to_file) as json_file:
			json_data = json.load(json_file)
		return json_data

	def search_json(json_data, request_str):
		found = 0
		group_id = None
		import_type = None
		for items in json_data['import']:
			#str = 
			if request_str == items['call_command'] or request_str.find(items['call_command']) != -1:
				found = 1
				group_id = items['group_id']
				self.group_id = group_id
				break
		return 1 if found == 1 else 0