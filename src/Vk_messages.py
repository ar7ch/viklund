#This file is part of viklund.
#
#Viklund is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Viklund is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with viklund.  If not, see <http://www.gnu.org/licenses/>.

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

	@staticmethod
	def handle_id_request(item):
		user = viklund.vkApi.users.get(user_ids=item[u'user_id'])
		username = user[0]['first_name'] + ' ' + user[0]['last_name']
		user = None
		viklund.Message.send_selective(item, 'msg', username + ': ' + str(item[u'user_id']))
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
	def is_chat(item):
		"""Check if is current request from chat or from private message"""

		if u'chat_id' in item and item[u'chat_id'] != u'':
			return viklund.Message.CONVERSATION
		else:
			return viklund.Message.PRIVATE_MESSAGE
	@staticmethod
	def send_attachments(dest_id, attachments, dest_type):
		"""
		Sends list of attachments to user or chat

		Sends list of attachments (with attachment syntax <type><owner_id>_<media_id>_<access_key>) to user or chat
		
		Parameters
		----------
		dest_id : string 
			Destination id (chat_id or user_id)
		attachments : list
			List of attachments with attachment syntax <type><owner_id>_<media_id>_<access_key> to send (access key is optional)
			Note that 0th element is reserved for text.
		dest_type
			Destination type of current response. Can be either Message.CONVERSATION or Message.PRIVATE_MESSAGE
		Raises
		-------
			ValueError
				If got invalid dest_type value
			Exception

		"""
		"""Messages.send() vk_api method excepts list of attachments to send as string where attachments are separated with comma""" 
		
		try:
			if dest_type != Message.PRIVATE_MESSAGE or dest_type != Message.CONVERSATION:
				raise ValueError("Invalid dest_type value")
		attachment_str = ','.join(attachments[1:]) #separate attachments list with comma starting with second element (first one is reserved for text)
		message_str = None
		if not attachments[0]: #if there is no text
			message_str = ' '	
		try:
			if dest_type == Message.PRIVATE_MESSAGE:
				viklund.vk.method('messages.send', {'user_id':dest_id, 'message':message_str, 'attachment':attachment_str})
			elif dest_type == Message.CONVERSATION:
				viklund.vk.method('messages.send', {'chat_id':dest_id, 'message':message_str, 'attachment':attachment_str})
		except vk_api.VkApiError:
			raise
		except vk_api.ApiError:
			raise

	@staticmethod
	def send_pic(user_id, pic_id):
		viklund.vk.method('messages.send', {'user_id':user_id, 'attachment':pic_id})
	@staticmethod
	def send_pic_chat(chat_id, pic_id):
		viklund.vk.method('messages.send', {'chat_id':chat_id, 'attachment':pic_id})
	@staticmethod
	def send_wall_post(user_id, post):
		viklund.vk.method('messages.send', {'user_id':user_id, 'attachment':post})
	@staticmethod
	def send_wall_post_chat(chat_id, post):
		viklund.vk.method('messages.send', {'chat_id':chat_id, 'attachment':post})
	@staticmethod
	def write_msg(user_id, s):
	    viklund.vk.method('messages.send', {'user_id':user_id,'message':s})
	@staticmethod
	def write_msg_chat(chat_id, s):
		viklund.vk.method('messages.send', {'chat_id':chat_id,'message':s})
