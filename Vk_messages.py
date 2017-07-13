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
