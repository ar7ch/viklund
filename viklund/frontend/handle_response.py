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
import time
import os, sys
from datetime import datetime
import random

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
			not_found_string = 'Request not found: {}\n/help for help message, /post for available imports\n'.format(request)
			no_request_string = 'Usage: /post (-random) <request>\nAvailable imports: \n{}'.format('\n'.join(requests.keys()))
			if not request:
				viklund.Message.send(message_text = no_request_string)
			else:
				viklund.Message.send(message_text = not_found_string)
				raise KeyError(not_found_string)
			return
		#TODO: send more than 1 post
		if '-random' in arguments:
			# random offset requires calling get_post() to get posts count
			post_resp = viklund.PostImport.get_post(post_values)
			post_count = post_resp['count']
			post_values['offset'] = random.randint(0, post_count - 1)

		response = viklund.PostImport.get_post(post_values)
		post_items = response['items']
		for post_item in post_items:
			post_text = ''
			if post_item['text']:
				post_text = post_item['text']
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
		if separated[0] == '-':
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
		viklund.Message.send(message_text='Nothing to resend')
		return -1
	viklund.Message.send(attachments = attachments_list)

def handle_response(item):
	"""
	Setup is done - here goes your bot's response code!
	There are some essential methods that may be useful.
	"""
	viklund.Message.setup_dest(item) #setup dest_id and dest_type to reply
	request_str = item[u'body'].lower()
	sep = request_str.split() 
	command = sep[0][1:] # remove slash char
	arguments = parse_request_args(sep)
	request = parse_request(sep, arguments)
	try:
		if command == 'post':
			handle_post_request(arguments, request, item)
		elif command == 'wiki':
			viklund.Extra.handle_wiki_search(request)
		elif command == 'info':
			handle_info_request(item, request)
		elif command == 'resend':
			handle_resend_request(item)
		elif command == 'status':
			status_message = '''
			Viklund Bot v.0.6
			Status: working
			Time on server: {}
			'''.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		elif command == 'help':
			help_message = '''
			Viklund Bot v.0.6\n
			Commands:
			/post [-random] <request> - send post from pre-configured list of imports. Sends latest post by default, use -random option to send random post.\n
			/wiki <request> - search in Wikipedia.\n
			/resend - resend media attached to message\n
			/info <id> - show user's name, domain and id. Specify ID to send other user's info.\n    
			/status - show bot status.\n
			/help - print this help message and exit.\n
			'''#/weather <request> - show weather for specified location.\n
			viklund.Message.send(message_text=help_message)
		else:
			viklund.Message.send(message_text = '{}: command not found\n/help for help'.format(command))
	except Exception as e:
		raise