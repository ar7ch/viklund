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
import wikipedia

class Message:
	#constants to select destination type
	PRIVATE_MESSAGE = 1
	CONVERSATION = 0
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
	@staticmethod
	def get_message(values={'out': 0,'count': 100,'time_offset': 60}):
		"""
		Get message. Wrapper for VK API's messages.get() method. 
		<https://vk.com/dev/messages.get>

		Parameters
		----------
		value : list 
			Item section of response string.
		
		Raises
		______
			vk_api.VkApiError
				VK API errors.
			vk_api.ApiError
				VK API errors.
		Returns
		-------
		list
			List of attachment strings. Note that 0th element is reserved for text
		"""
		try:
			response = viklund.vk.method('messages.get', values)
		except vk_api.VkApiError:
			raise
		except vk_api.ApiError:
			raise
		return response['items']
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
		list
			List of attachment strings. Note that 0th element is reserved for text
		"""
		attachments = []
		attachments[0] = '' #note that 0th element is reserved for text 
		if item['text']: #if string is not empty
			attachments[0] = item['text']
		for attachment in item['attachments']:
			#attachment syntax is <type><owner_id>_<media_id>_<access_key>
			att_string = ''
			att_type = attachment['type']
			att_owner_id = attachment[att_type]['owner_id']
			att_media_id = attachment[att_type]['media_id']
			att_access_key = ''
			if u'access_key' in attachment[att_type]:
				att_access_key = '_' + attachment[att_type][access_key]
			att_string = att_type + att_owner_id + '_' + att_media_id + access_key
			attachments.append(att_string)
		#if not attachments: #check if list is empty
			#raise exception
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
			if dest_type != Message.PRIVATE_MESSAGE or dest_type != Message.CONVERSATION:
				raise ValueError("Invalid dest_type value")
		attachment_str = ','.join(attachments) #separate attachments list with commas	
		try:
			if dest_type == Message.PRIVATE_MESSAGE:
				viklund.vk.method('messages.send', {'user_id':dest_id, 'message':message_text, 'attachment':attachment_str})
			elif dest_type == Message.CONVERSATION:
				viklund.vk.method('messages.send', {'chat_id':dest_id, 'message':message_text, 'attachment':attachment_str})
		except vk_api.VkApiError:
			raise
		except vk_api.ApiError:
			raise