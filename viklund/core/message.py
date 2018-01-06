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

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
import sys
import viklund
import time

class Message:
	#constants to select destination type
	PRIVATE_MESSAGE = 1
	CONVERSATION = 0

	@staticmethod
	def setup_dest(item):
		"""
		Setup destination id. Wrapper for get_dest_type() and get_dest_id()
		
		Parameters
		----------
			item
				Item section of response.

		"""
		viklund.dest_type = viklund.Message.get_dest_type(item)
		viklund.dest_id = viklund.Message.get_dest_id(item)
	
	@staticmethod
	def get_dest_id(item):
		"""
		Get dest_id - chat_id or user id.

		Parameters
		----------
			item
				Item section of response.

		Returns
		-------
			item['user_id']
				If destination id is user id
			item['chat_id']
				If destination id is chat_id


		"""
		dest_type = viklund.Message.get_dest_type(item)
		if dest_type == viklund.Message.PRIVATE_MESSAGE:
			return item['user_id']
		else:
			return item['chat_id']
	@staticmethod
	def handle_message():
		"""
		Primary messages handling function.
		Wait for message, get, fork if available and pass to handle_response.

		Raises
		______
			Exception
				Exceptions ocurred.
		"""
		values = {'out': 0,'count': 100,'time_offset': 60}
		fork_count = 0
		FORK_LIMIT = 5
		while True:
			try:
				if viklund.Message.wait_message():
					response = viklund.Message.get_message(values)
				if response:
					last_message_id = response['items'][0]['id']
					values['last_message_id'] = last_message_id #save last message id to prevent handling the same message twice
					items = response['items']
					for item in items:
						if item['body'] and item['body'][0] == '/':
							print(viklund.Logging.log_messages(item))
							# fork process for handle_response() execution if available 
							#if fork_count <= FORK_LIMIT:
							#	fork_count += 1
							#	pid = os.fork()
							#	if not pid: # if in child process
							#		viklund.handle_response(item)
							#		exit(0) # child process must be closed after the work is done
							#else:
								#else call function in the same process
							viklund.handle_response(item)
							del item
			except Exception as e:
				viklund.Logging.write_log(viklund.Logging.warning(e))
			time.sleep(1)

	@staticmethod
	def wait_message():
		"""
		Wait for new event (message) using Long Poll

		Returns
		-------
		: bool
			True if got new message event, false if error occured.
		"""
		longpoll = VkLongPoll(viklund.vk_session)
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW:
				return True
		return False
	@staticmethod
	def get_message(values):
		"""
		Get message. Wrapper for VK API's messages.get() method. 
		<https://vk.com/dev/messages.get>

		Parameters
		----------
		values : dict 
			Item section of response string.
		
		Raises
		______
			vk_api.VkApiError
				VK API errors.
			vk_api.ApiError
				VK API errors.
		Returns
		-------
		response
			Response of messages.get() method.		
		"""
		try:
			response = viklund.vk_session.method('messages.get', values)
		except vk_api.VkApiError:
			raise
		except vk_api.ApiError:
			raise
		return response
	@staticmethod
	def parse_attachments(item):
		"""
		Parse attachments from response item.

		Parse attachments from response item and return a list of attachment strings.
		
		Parameters
		----------
		item 
			Item section of response.

		Returns
		-------
		attachments : list
			List of attachment strings.
		"""
		attachments = []
		if 'attachments' in item:
			for attachment in item['attachments']:
				#attachment syntax is <type><owner_id>_<media_id>_<access_key>
				att_string = ''
				att_type = attachment['type']
				att_owner_id = attachment[att_type]['owner_id']
				att_media_id = attachment[att_type]['id']
				att_access_key = ''
				if u'access_key' in attachment[att_type]:
					att_access_key = '_' + attachment[att_type]['access_key']
				att_string = '{0}{1}_{2}{3}'.format(att_type,str(att_owner_id),str(att_media_id),att_access_key)
				attachments.append(att_string)
		return attachments
	@staticmethod
	def get_dest_type(item):
		"""
		Check if is current request from chat or from private message

		Parameters
		----------
			item
				Item section of response.
		Returns
		-------
			viklund.Message.CONVERSATION
				If current request came from chat.
			viklund.Message.PRIVATE_MESSAGE
				If current request came from private messages.
		"""

		if u'chat_id' in item and item[u'chat_id'] != u'':
			return viklund.Message.CONVERSATION
		else:
			return viklund.Message.PRIVATE_MESSAGE
	@staticmethod
	def send(send_dest_id=None, send_dest_type=None, message_text = '', attachments = ''):
		"""
		Send message to user or conversation

		Send message to user of conversation. Attachments are expected as list of attachment strings 
		with attachment syntax <type><owner_id>_<media_id>_<access_key> (access_key is optional)
		
		Parameters
		----------
		send_dest_id : string 
			Destination id (chat_id or user_id)
		send_dest_type
			Destination type of current response. Can be either Message.CONVERSATION or Message.PRIVATE_MESSAGE
		attachments : string list
			List of attachments with attachment syntax <type><owner_id>_<media_id>_<access_key> to send (access key is optional)
		message_text : string
			Text to send.
		Raises
		-------
			ValueError
				If got invalid dest_type value
			vk_api.VkApiError
				VK API errors.
			vk_api.ApiError
				VK API errors.
		"""
		"""Messages.send() vk_api method excepts list of attachments to send as string where attachments are separated with comma""" 
		
		if not send_dest_id: #python gives attribute_error if viklund.dest_id is default value of send_dest_id argument, no idea why
			send_dest_id = viklund.dest_id
		if not send_dest_type:
			send_dest_type = viklund.dest_type
		
		try:
			if send_dest_type != Message.PRIVATE_MESSAGE and send_dest_type != Message.CONVERSATION:
				raise ValueError("Invalid dest_type value")
		except ValueError:
			raise
		attachment_str = ','.join(attachments) #separate attachments list with commas	
		try:
			if send_dest_type == Message.PRIVATE_MESSAGE:
				viklund.vk_session.method('messages.send', {'user_id':send_dest_id, 'message':message_text, 'attachment':attachment_str})
			elif send_dest_type == Message.CONVERSATION:	
				viklund.vk_session.method('messages.send', {'chat_id':send_dest_id, 'message':message_text, 'attachment':attachment_str})
		except vk_api.VkApiError:
			raise
		except vk_api.ApiError:
			raise