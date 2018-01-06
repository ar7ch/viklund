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
import time
import os, sys
from datetime import datetime
import random

def handle_post_request(arguments, request, item):
	# step 0: configure sending options
	# step 1: find if request is in .json config
	# step 2: get post
	# step 3: send it to user
	try:
		dest_type = viklund.Message.get_dest_type(item)
		dest_id = viklund.Message.get_dest_id(item)
		offset = 0
		json_data = viklund.JsonParser.read_json(viklund.JSON_PATH)
		requests = viklund.JsonParser.parse_import(json_data)
		import_id = None
		if request in requests:
			import_id = requests[request]
		else:
			err_string = 'Request not found: {}'.format(request)
			viklund.Message.send(dest_id = dest_id, dest_type = dest_type, message_text = err_string)
			raise KeyError(err_string)
			return
		#TODO: send more than 1 post

		post_resp = viklund.PostImport.get_post({'owner_id':import_id, 'count':1, 'offset':2})
		post_count = post_resp['count']

		if '-random' in arguments:
			offset = random.randint(0, post_count - 1)
		response = viklund.PostImport.get_post({'owner_id':import_id, 'count':1, 'offset':offset})
		post_items = response['items']
		for post_item in post_items:
			post_text = ''
			if post_item['text']:
				post_text = post_item['text']
			attachments_list = viklund.Message.parse_attachments(post_item)
			viklund.Message.send(dest_id, dest_type, message_text = post_text, attachments = attachments_list)
	except Exception as e:
		raise

def parse_request_args(sep):
	arguments = []
	for separated in sep[1:]:
		#argument syntax is /command -arg1 -arg2 request
		if separated[0] == '-':
			arguments.append(separated)
	return arguments

def parse_request(sep):
	request = None
	for separated in sep[1:]:
		if separated[0] != '-':
			return separated

def handle_response(item):
	"""
	Setup is done - here goes your bot's response code!
	There are some essential methods that may be useful.
	"""
	request_str = item[u'body'].lower()
	sep = request_str.split()
	command = sep[0][1:] # remove slash char
	arguments = parse_request_args(sep)
	request = parse_request(sep)
	try:
		if command == 'post':
			handle_post_request(arguments, request, item)
	except Exception as e:
		raise


	"""
	if received_str.find(u'рандом') != -1:
		viklund.Vk_random.handle_random(item, received_str)
	elif received_str.find(u'пост') != -1:
		viklund.Vk_group_import.handle_import_request(item, received_str)
	elif received_str.find(u'перешли') != -1:
		viklund.Vk_messages.resend_user_message(item, received_str)
	elif received_str.find(u'айди') != -1:
		viklund.Vk_messages.handle_id_request(item)
	elif received_str.find(u'вики') != -1:
		viklund.Vk_messages.handle_wiki_search_request(item, received_str)
	elif received_str.find(u'помощь') != -1:
		viklund.Vk_messages.send_selective(item, 'msg', 'Viklund Bot\nИспользование: \'/команда\'\nДоступные команды:\nпост\nрандом\nперешли\nайди\nпомощь')
	elif received_str.find(u'статус') != -1:
			viklund.Vk_messages.send_selective(item, 'msg', 'Viklund v.0.4\nСтатус: up\nВремя на сервере: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	else:
		viklund.Vk_messages.send_selective(item, 'msg', received_str[1:] + ': команда не найдена')
		received_str = u''
	"""