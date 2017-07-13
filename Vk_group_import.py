import time
import vk_api
import random
import json
import os
import sys
import getpass
import viklund

class Vk_group_import:
	group_id = None
	posts_count = None
	import_type = None
	def get_group_id(self):
		return self.group_id
	def set_group_id(self, value):
		self.group_id = value
	def get_posts_count(self):
		return self.posts_count
	def set_posts_count(self, value):
		self.posts_count = value
	def get_import_type(self):
		return self.import_type
	def set_import_type(self, value):
		self.group_id = value
	def select_and_send_random_group_thing(self, group_id, posts_count, item, type_flag):
		watchdog_counter = 0
		posts = viklund.vkApi.wall.get(owner_id = group_id)
		self.set_posts_count(posts['count'])
		while True:
			group_wall = viklund.vkApi.wall.get(count = 1, offset = random.randint(1, self.get_posts_count()), owner_id = self.get_group_id()) 
			try:
				if type_flag == 'pic':
					pic = u'photo' + str(group_id) + '_' + str(group_wall['items'][0]['attachments'][0]['photo']['id'])
					viklund.Vk_messages.send_selective(item, 'pic', pic)
				elif type_flag == 'msg':
					msg = group_wall['items'][0]['text']
					viklund.Vk_messages.send_selective(item, 'msg', msg)
				elif type_flag == 'wall':
					wall = u'wall' + str(group_id) + '_' + str(group_wall['items'][0]['id'])
					viklund.Vk_messages.send_selective(item, 'wall', wall)
				return 1
			except:
				if watchdog_counter > 100:
					viklund.Vk_messages.send_selective(item, 'msg', u'Что-то пошло не так. Попробуйте еще раз')
					return -1
				watchdog_counter += 1
				continue
	def get_request_str(self, recieved_str):
		start_index = recieved_str.find('пост')
		start_index += 4
		request_str = ''
		for i in range(start_index, len(recieved_str)):
			if recieved_str[i].isalpha() or recieved_str[i].isdigit():
				request_str += recieved_str[i]
		return request_str
	def get_import_list(self, item, json_data, filename):
		commands = ''
		for items in json_data[filename]:
			commands += items['call_command'] + '\n'
		viklund.Vk_messages.send_selective(item, 'msg', 'Доступные команды:\n' + commands)

	def handle_import_request(self, item, recieved_str):
		request = self.get_request_str(recieved_str)
		if viklund.Vk_messages.check_if_chat(item):
			chat_id = item[u'chat_id']
		try:
			json_data = self.read_json('default')
			default_search_result = self.search_json(json_data, request, 'default')
			if request == '':
				self.get_import_list(item, json_data, 'default');
				return 0
			#if not default_search_result:
			#if not viklund.Vk_messages.check_if_chat(item):
			if not default_search_result:
				raise Import_command_not_found_exception()
				#json_data = self.read_json('chat_id'+str(chat_id))
				#chat_search_result = self.search_json(json_data, request, 'chat_id'+str(chat_id))
				#if default_search_result or chat_search_result:
				#	raise Import_command_not_found_exception()
		except viklund.Private_messages_import_prohibited_exception:
			viklund.Vk_messages.send_selective(item, 'msg', request + 'Извините, в личных сообщениях доступны только стандартные импорты!')
			return 3
		except Import_command_not_found_exception:
			viklund.Vk_messages.send_selective(item, 'msg', request + ': запрос не найден')
			return 2
		else:
			self.select_and_send_random_group_thing(self.get_group_id(), self.get_posts_count(), item, self.get_import_type()) 
	
	def read_json(self, filename):
		pathname = os.path.abspath(os.path.dirname(sys.argv[0])) #get absolute path current dir (where the script is)
		pathname = os.path.join(pathname, 'vk_json_tables')
		with open(pathname + '/' + filename + '.json') as json_file:
			json_data = json.load(json_file)
		return json_data
	def search_json(self, json_data, request_str, filename):
		found = 0
		group_id = None
		import_type = None
		for items in json_data[filename]:
			#str = 
			if request_str == items['call_command'] or request_str.find(items['call_command']) != -1:
				found = 1
				group_id = items['group_id']
				import_type = items['import_type']
				self.group_id = group_id
				self.import_type = import_type
				break
		return 1 if found == 1 else 0

class Import_command_not_found_exception(Exception):
	def __init__(self):
		pass
class Private_messages_import_prohibited_exception(Exception):
	def __init__(self):
		pass