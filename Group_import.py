import time
import vk_api
import random
import json
import os
import sys
import getpass
import viklund

class Group_import:
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
		while True:
			group_wall = vkApi.wall.get(count = 1, offset = random.randint(1, posts_count / 2), owner_id = group_id) 
			if type_flag == 'pic':
				try:
					pic = u'photo' + str(group_id) + '_' + str(group_wall['items'][0]['attachments'][0]['photo']['id'])
					Vk_messages.send_selective(item, 'pic', pic)
					return 1
				except:
					if watchdog_counter > 100:
						Vk_messages.send_selective(item, 'msg', u'Что-то пошло не так. Попробуйте еще раз')
						return -1
					watchdog_counter += 1
					continue
			elif type_flag == 'msg':
				try:
					Vk_messages.send_selective(item, 'msg', group_wall['items'][0]['text'])
					return 1
				except:
					if watchdog_counter > 100:
						Vk_messages.send_selective(item, 'msg', u'Что-то пошло не так. Попробуйте еще раз')
						return -1
					watchdog_counter += 1
					continue

	def get_request_str(self, recieved_str):
		#we could use endless 'elif's, but we won't
		start_index = recieved_str.find('пост')
		start_index += 4
		request_str = ''
		for i in range(start_index, len(recieved_str)):
			if recieved_str[i].isalpha():
				request_str += recieved_str[i]
		return request_str
	def handle_import_request(self, item, recieved_str):
		request = self.get_request_str(recieved_str)
		if Vk_messages.check_if_chat(item):
			chat_id = item[u'chat_id']
		try:
			json_data = self.read_json('default')
			default_search_result = self.search_json(json_data, request, 'default')
			print(str(self.group_id))
			print('request is' + request)
			print(self.group_id)
			print(self.posts_count)
			print(self.import_type)
			if not default_search_result:
				if not Vk_messages.check_if_chat(item):
					raise Private_messages_import_prohibited_exception()
				json_data = self.read_json('chat_id'+str(chat_id))
				chat_search_result = self.search_json(json_data, request, 'chat_id'+str(chat_id))
				if default_search_result or chat_search_result:
					raise Import_command_not_found_exception()
		except Private_messages_import_prohibited_exception:
			Vk_messages.send_selective(item, 'msg', request + 'Извините, в личных сообщениях доступны только стандартные импорты!')
		except Import_command_not_found_exception:
			Vk_messages.send_selective(item, 'msg', request + ': запрос не найден')
			return 2
		finally: #self, group_id, posts_count, item, type_flag
			self.select_and_send_random_group_thing(self.get_group_id(), self.get_posts_count(), item, self.get_import_type()) 
	
	def read_json(self, filename):
		pathname = os.path.abspath(os.path.dirname(sys.argv[0])) #get absolute path current dir (where the script is)
		pathname = os.path.join(pathname, 'lists')
		with open(pathname + '/' + filename + '.json') as json_file:
			json_data = json.load(json_file)
		return json_data
	def search_json(self, json_data, request_str, filename):
		found = 0
		group_id = None
		posts_count = None
		import_type = None
		for items in json_data[filename]:
			#str = 
			if request_str == items['call_command']:
				found = 1
				group_id = items['group_id']
				posts_count = items['posts_count']
				import_type = items['import_type']
				self.group_id = group_id
				self.posts_count = posts_count
				self.import_type = import_type
				break
		return 1 if found == 1 else 0
