import time
import vk_api
import random
import json
import os
import sys
import getpass
import viklund

class Vk_messages:
	@staticmethod
	def handle_id_request(item):
		user = viklund.vkApi.users.get(user_ids=item[u'user_id'])
		username = user[0]['first_name'] + ' ' + user[0]['last_name']
		user = None
		viklund.Vk_messages.send_selective(item, 'msg', username + ': ' + str(item[u'user_id']))
	@staticmethod
	def handle_messages():
		values = {'out': 0,'count': 100,'time_offset': 60}
		while True:
			response = viklund.vk.method('messages.get', values)
			if response['items']:
				values['last_message_id'] = response['items'][0]['id']
			for item in response['items']:
				recieved_str = item[u'body'].lower()
				viklund.Vk_system.print_log(item, recieved_str, None)
				if recieved_str.find(u'лит') != -1 and recieved_str.find(u'рандом') != -1:
					viklund.Vk_random.handle_random(item, recieved_str)
				elif recieved_str.find(u'лит') != -1 and recieved_str.find(u'пост') != -1:
					viklund.Vk_group_import.handle_import_request(item, recieved_str)
				elif recieved_str.find(u'лит') != -1 and recieved_str.find(u'перешли') != -1:
					viklund.Vk_messages.resend_user_message(item, recieved_str)
				elif recieved_str.find(u'лит') != -1 and recieved_str.find(u'айди') != -1:
					viklund.Vk_messages.handle_id_request(item)
			recieved_str = u''
			time.sleep(1)
	@staticmethod
	def resend_user_message(item, recieved_str):
		try:
			access_key = ''
			try:
				access_key = '_' + str(item['attachments'][0]['photo']['access_key'])
			except:
				access_key = ''
			pic = u'photo' + str(item['attachments'][0]['photo']['owner_id']) + '_' + str(item['attachments'][0]['photo']['id']) + access_key
			viklund.Vk_messages.send_selective(item, 'pic', pic)
		except Exception as e:
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
