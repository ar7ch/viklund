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

import threading
import viklund
import time
import os, sys
from datetime import datetime
import random

def handle_response(item):
	""" no idea how to call this, so i call this frontend"""
	
	"""
	This file implement user's interaction with bot - commands and responses to commands.
	You can edit this file freely because there is no function that Viklund core functions depend on.
	Except handle_response() - it is the function where message item are sent to for you to handle user request.
	Please do not change this function's name and arguments if you are not going to edit Viklund core code.
	"""

	"""
	Setup is done - here goes your bot's response code!
	There are some essential methods that may be useful.
	"""
	request_str = item[u'body']
	sep = request_str.split() 
	command = sep[0][1:].lower() # remove slash char
	arguments = parse_request_args(sep)
	request = parse_request(sep, arguments)
	try:
		response(item, request, command, arguments)
	except Exception as e:
		exception_message = None
		if hasattr(e, 'message'):
			exception_message = e.message().strip('\'')
		else:
			exception_message = str(e)
		print(viklund.Logging.warning(e))


def response(item, request, command, arguments):
	try:
		if command == 'пост':
			handle_post_request(arguments, request, item)
		elif command == 'вики':
			viklund.Extra.handle_wiki_search(request)
		elif command == 'инфо':
			handle_info_request(item, request)
		elif command == 'перешли':
			handle_resend_request(item)
		elif command == 'перевод':
			viklund.Extra.handle_translate_request(request, arguments)
		elif command == 'статус':
			handle_status_request()
		elif command == 'помощь':
			handle_help_request()
		else:
			handle_not_found(command)
	except Exception:
		raise
def handle_status_request():
	status_message = '''
	Viklund Bot v.0.6
	Статус: работает
	Время на сервере: {}
	'''.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	viklund.Message.send(message_text=status_message)

def handle_not_found(command):
	not_found_message = '{}: команда не найдена\n/помощь для справки'.format(command)
	viklund.Message.send(message_text=not_found_message)

def handle_help_request():
	help_message = '''
	Viklund Bot v.0.6
	Доступные команды:

	/пост [-рандом] <запрос> - отправить пост из списка источников. По умолчанию отправляет самый свежий пост, используйте опцию -рандом, чтобы отправить случайный пост.
	
	/вики <запрос> - поиск в Википедии.
	
	/перевод [-(код языка оригинала)] [-(код языка, на который нужно перевести)] <запрос> - перевод с одного языка на другой.
	По умолчанию переводит с любого языка на русский и с русского на английский.

	/перешли - переслать медиа (фотографии, документы и т.д.), прикрепленные к сообщению.
	
	/инфо <id> - показать информацию о пользователе. Укажите ID, чтобы показать информацию для другого пользователя.  
	
	/статус - показать статус бота.
	
	/помощь - показать это сообщение.
	'''#/weather <request> - show weather for specified location.\n
	viklund.Message.send(message_text=help_message)
def handle_post_request(arguments, request, item, post_values = {'owner_id':None, 'count':1, 'offset':0}):
	"""
	Implementation of /post command. 

	Send imported post to user.
	
	Parameters
	-----------
		arguments : list
			Arguments parsed.
		request : string
			Request string.
		item
			Item section of response.
		post_values  : dict
			Values to pass to get_message() method.
	Raises
	------
		Exception
			Exceptions occured.
	"""

	# step 0: configure sending options
	# step 1: find if request is in .json config
	# step 2: get post
	# step 3: send it to user
	try:
		json_data = viklund.JsonParser.read_json(viklund.JSON_PATH)
		requests = viklund.JsonParser.parse_import(json_data)
		if request in requests:
			post_values['owner_id'] = requests[request]
		else:
			log_not_found_string = 'Пользовательский запрос не найден: {}'.format(request)
			not_found_string = 'Запрос не найден: {}\n/помощь для справки, /пост для доступных импортов\n'.format(request)
			no_request_string = 'Использование: /пост (-рандом) <запрос>\nДоступные импорты: \n{}'.format('\n'.join(requests.keys()))
			if not request:
				viklund.Message.send(message_text = no_request_string)
			else:
				viklund.Message.send(message_text = not_found_string)
				raise KeyError(log_not_found_string)
			return
		post_resp = viklund.PostImport.get_post(post_values) # random offset requires calling get_post() to get posts count 				
		if 'is_pinned' in post_resp['items'][0] and post_resp['items'][0]['is_pinned']:
			post_values['offset'] += 1
		if '-рандом' in arguments:
			post_count = post_resp['count']
			post_values['offset'] = random.randint(0, post_count - 1)
		response = viklund.PostImport.get_post(post_values)
		if not 'items' in response:
			viklund.Message.send(message_text = u'Произошла ошибка!')
		post_items = response['items']
		for post_item in post_items:
			post_text = viklund.Message.parse_text_attachments(post_item)
			attachments_list = viklund.Message.parse_attachments(post_item)
			viklund.Message.send(message_text = post_text, attachments = attachments_list)
	except Exception as e:
		raise

def parse_request_args(sep):
	"""
	Parse args from user's message.
	
	Parameters
	-----------
		sep : list
			Whitespace-separated user messages.
	Returns
	-------
		arguments : list
			List of parsed arguments.
	"""
	arguments = []
	for separated in sep[1:]:
		#argument syntax is /command -arg1 -arg2 request
		if separated[0] == '-' and len(separated) > 1:
			arguments.append(separated)
	return arguments

def parse_request(sep, arguments):
	"""
	Parse request from user's message.

	Parameters
	-----------
		sep : list
			Whitespace-separated user message.
		arguments : list
			Arguments parsed with parse_request_args().
	Returns
	-------
		request : string
			Request string.

	"""
	request_str = ''
	for separated in sep[1:]:
		if not (separated in arguments):
			request_str += separated + ' '
	return request_str.strip()

def handle_info_request(item, request=None):
	"""
	Implementation of /info command - get user info. 
	
	Parameters
	-----------
		item
			Item section of response.
		request
			Custom ID. None by default.
	"""
	user_id = None
	if request:
		user_id = request
	else:
		user_id = item['user_id']
	#request_str = 'https://vk.com/foaf.php?id={}'.format(target_id)
	#with urllib.request.urlopen(request_str) as response:
	#	rdf_response = response.read()
	response = viklund.vk_session.method('users.get', {'fields':'domain', 'user_ids':user_id})
	first_name = response[0]['first_name']
	last_name = response[0]['last_name']
	domain = response[0]['domain']
	ans_str = '{0} {1}\nID: {2}\nDomain: {3}'.format(first_name, last_name, str(user_id), domain)

	viklund.Message.send(message_text=ans_str)

def handle_resend_request(item):
	"""
	Implementation of /resend command - resend user's attachments.
	
	Parameters
	-----------
		item
			Item section of response.
	"""
	attachments_list = viklund.Message.parse_attachments(item)
	if not attachments_list:
		viklund.Message.send(message_text='Нечего пересылать')
		return -1
	viklund.Message.send(attachments = attachments_list)

