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
			List of attachment strings.
		"""
		attachments = []
		if item['text']: #if string is not empty
			attachments.append(item['text'])
		for attachment in item['attachments']:
			#attachment syntax is <type><owner_id>_<media_id>
			att_string = ''
			att_type = attachment['type']
			att_owner_id = attachment[att_type]['owner_id']
			att_media_id = attachment[att_type]['media_id']
			att_access_key = ''
			if u'access_key' in attachment[att_type]:
				att_access_key = '_' + attachment[att_type][access_key]
			att_string = att_type + att_owner_id + '_' + att_media_id + access_key
			attachments.append(att_string)
	@staticmethod
	def is_chat(item):
		if u'chat_id' in item and item[u'chat_id'] != u'':
			return True
		else:
			return False
	@staticmethod
	def send(item, attachments):
		
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
