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

import viklund
import wikipedia
class Extra:
	@staticmethod
	def handle_wiki_search(search_request):
		"""
		Search for request on Wikipedia.

		Parameters
		----------
		search_request : string 
			Request to find.
		
		Raises
		______
			wikipedia.PageError:
				If page doesn't exist
			wikipedia.DisambiguationError
				If page is a disambiguation page.
			Exception
				Other possible errors.
		"""
		wikipedia.set_lang("ru")
		try:
			search_result = wikipedia.summary(search_request)
			viklund.Message.send(message_text=search_result)
		except wikipedia.PageError:
			viklund.Message.send(message_text= '{}: not found'.format(search_request))
			raise
			return
		except wikipedia.DisambiguationError as e:
			viklund.message.send(message_text=e.options)
			raise
			return
		except:
			viklund.Message.send(message_text='An error occurred while searching')
			raise
	def handle_weather_request(request): #coming soon
		pass