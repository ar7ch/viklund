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
		Returns
		-------

		"""
		response = None
		try:
			response = viklund.vk_session.method('wall.get', values)
		except vk_api.VkApiError:
			raise
		except vk_api.ApiError:
			raise
		return response
