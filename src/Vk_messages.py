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

class Vk_messages:
	@staticmethod
	def handle_id_request(item):
		user = viklund.vkApi.users.get(user_ids=item[u'user_id'])
		username = user[0]['first_name'] + ' ' + user[0]['last_name']
		user = None
		viklund.Vk_messages.send_selective(item, 'msg', username + ': ' + str(item[u'user_id']))
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
				viklund.Vk_messages.send_selective(item, 'pic', pic)
		except Exception as e:
			print(e)
			Vk_messages.send_selective(item, 'msg', u'Произошла ошибка!')
			return -1
	@staticmethod
	def check_if_chat(item):
		if u'chat_id' in item and item[u'chat_id'] != u'':
			return True
		else:
			return False
	@staticmethod
	def send_selective(item, send_type, send_item):
		if send_type == 'pic':
			if viklund.Vk_messages.check_if_chat(item):
				viklund.Vk_messages.send_pic_chat(item[u'chat_id'], send_item)
			else:
				viklund.Vk_messages.send_pic(item[u'user_id'], send_item)
		elif send_type == 'msg':
			if Vk_messages.check_if_chat(item):
				viklund.Vk_messages.write_msg_chat(item[u'chat_id'], send_item)
			else:
				viklund.Vk_messages.write_msg(item[u'user_id'], send_item)
		elif send_type == 'wall':
			if Vk_messages.check_if_chat(item):
				viklund.Vk_messages.send_wall_post_chat(item[u'chat_id'], send_item)
			else:
				viklund.Vk_messages.send_wall_post(item[u'user_id'], send_item)
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
