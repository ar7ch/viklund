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
import wikipedia
import time

class Message:
	#constants to select destination type
	PRIVATE_MESSAGE = 1
	CONVERSATION = 0

	@staticmethod
	def get_dest_id(item):
		dest_type = viklund.Message.get_dest_type(item)
		if dest_type == viklund.Message.PRIVATE_MESSAGE:
			return item[u'user_id']
		else:
			return item[u'chat_id']
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
					print('Got message event')
					response = viklund.Message.get_message(values)
					print('Got message')
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
							#	if pid == 0: # if in child process
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
		items : dict
			Dictionary of message items.		
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
		Parse attachments from response string.

		Parse arguments from response item string and return a list of attachment strings.
		
		Parameters
		----------
		item 
			Item section of response string.

		Returns
		-------
		attachments : list
			List of attachment strings.
		"""
		attachments = []
		if 'attachments' in item:
			print('attachments:' + str(item['attachments']))
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
				print("Attachment is " + str(att_string))
				attachments.append(att_string)
		return attachments
	@staticmethod
	def get_dest_type(item):
		"""Check if is current request from chat or from private message"""

		if u'chat_id' in item and item[u'chat_id'] != u'':
			return viklund.Message.CONVERSATION
		else:
			return viklund.Message.PRIVATE_MESSAGE
	@staticmethod
	def send(dest_id, dest_type, message_text = '', attachments = ''):
		"""
		Send message to user or conversation

		Send message to user of conversation. Attachments are expected as list of attachment strings 
		with attachment syntax <type><owner_id>_<media_id>_<access_key> (access_key is optional)
		
		Parameters
		----------
		dest_id : string 
			Destination id (chat_id or user_id)
		dest_type
			Destination type of current response. Can be either Message.CONVERSATION or Message.PRIVATE_MESSAGE
		attachments : string list
			List of attachments with attachment syntax <type><owner_id>_<media_id>_<access_key> to send (access key is optional)
		message_text
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
		
		try:
			if dest_type != Message.PRIVATE_MESSAGE and dest_type != Message.CONVERSATION:
				raise ValueError("Invalid dest_type value")
		except ValueError:
			raise
		attachment_str = ','.join(attachments) #separate attachments list with commas	
		try:
			if dest_type == Message.PRIVATE_MESSAGE:
				viklund.vk_session.method('messages.send', {'user_id':dest_id, 'message':message_text, 'attachment':attachment_str})
			elif dest_type == Message.CONVERSATION:	
				viklund.vk_session.method('messages.send', {'chat_id':dest_id, 'message':message_text, 'attachment':attachment_str})
		except vk_api.VkApiError:
			raise
		except vk_api.ApiError:
			raise









	"""
	@staticmethod
	def resend_user_message(item, received_str): #TODO: send multiply pictures in one message, resend via forwarded messages
		try:
			for picture in item['attachments']:
				access_key = ''
				try:
					access_key = '_' + str(picture['photo']['access_key'])
				except:
					access_key = ''
				pic = u'photo' + str(picture['photo']['owner_id']) + '_' + str(picture['photo']['id']) + access_key
				viklund.Message.send_selective(item, 'pic', pic)
		except Exception as e:
			print(e)
			Message.send_selective(item, 'msg', u'Произошла ошибка!')
			return -1
	"""