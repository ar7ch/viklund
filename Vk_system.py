import time
import vk_api
import random
import json
import os
import errno
import sys
import getpass
import viklund
import configparser

class Vk_system():
	@staticmethod
	def get_policy_name(logs_policy):
		if logs_policy == 0:
			return 'no logs'
		elif logs_policy == 1:
			return 'write in file'
		elif logs_policy == 2:
			return 'stdout'
		else:
			return 'undefined'
	@staticmethod
	def ask_wrapper(input_text, options_list=[]):
		while True:
			i = input(input_text)
			if options_list == []:
				if i == 'y':
					return 1
				elif i == 'n':
					return 0
			else:
				if i in options_list:
					return i

	@staticmethod
	def ask_logs():
		config_file_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/viklund.conf'
		config_parser = configparser.RawConfigParser()
		config_parser.read(config_file_path) 
		try:
			viklund.logs_policy = int(config_parser.get('viklund-log', 'logs_policy'))
			if Vk_system.ask_wrapper('Your previous log policy was ' + Vk_system.get_policy_name(viklund.logs_policy) + '. Do you want to continue with it?(y/n)'):
				print('starting with logs policy ' + Vk_system.get_policy_name(viklund.logs_policy))
				return 0
			else:
				raise	
			if viklund.logs_policy == -1:
				raise
			if viklund.logs_policy < 0 or viklund.logs_policy > 2:
				print('config broken, repairing')
				raise
		except:
			if Vk_system.ask_wrapper('Would you like to log or output received messages and executed bot commands?(y/n):'):	
				log_answer = Vk_system.ask_wrapper('Would you like to log it in .log files like \"chat_id.log\" or output it via stdout? (file/stdout):', ['file', 'stdout'])
				if log_answer == 'file':
					try:
						logs_dir = os.path.dirname(sys.argv[0]) + '/vk_logs'
						print('OK, your logs will be there: ' + logs_dir)
						os.mkdir(os.path.abspath(logs_dir, 0o777))
					except OSError as e:
						if e.errno != errno.EEXIST:
							raise
					viklund.logs_policy = 1
				elif log_answer == 'stdout':
					viklund.logs_policy = 2
		config_parser.add_section('viklund-log')
		config_parser.set('viklund-log', 'logs_policy', str(viklund.logs_policy))
		with open(config_file_path, 'w') as config_file:
			config_parser.write(config_file)
		print('starting with logs policy ' + Vk_system.get_policy_name(viklund.logs_policy))	
	@staticmethod
	def print_log(item, recieved_str, type):
		if viklund.logs_policy == 1:
			pathname = os.path.abspath(os.path.dirname(sys.argv[0])) #get absolute path to current dir (where the script is)
			pathname = os.path.join(pathname, 'vk_logs')
			log_file = None
			if viklund.Vk_messages.check_if_chat(item):
				log_location = pathname + '/' + 'chat_' + str(item['chat_id']) + '.log'
			else:
				log_location = pathname + '/' + 'user_' + str(item['user_id']) + '.log'
			try:	
				log_file = open(log_location, 'x')
			except OSError:
				log_file = open(log_location, 'a')
			finally:
				viklund.Vk_system.log_selective(item, log_file, recieved_str)
				log_file.close()
		elif viklund.logs_policy == 2:
			viklund.Vk_system.log_selective(item, None, recieved_str)
	@staticmethod
	def log_selective(item, log_file, recieved_str):
		if viklund.logs_policy == 1:
			if viklund.Vk_messages.check_if_chat(item):
				log_file.write('user c id ' + str(item[u'user_id']) + ' в беседе с id ' + str(item[u'chat_id']) + ' написал: ' + recieved_str + '\n')
			else:
				log_file.write('user c id ' + str(item[u'user_id']) + ' написал: ' + recieved_str + '\n')
		elif viklund.logs_policy == 2:
			if viklund.Vk_messages.check_if_chat(item):
				print('user c id ' + str(item[u'user_id']) + ' в беседе с id ' + str(item[u'chat_id']) + ' написал: ' + recieved_str)
			else:
				print('user c id ' + str(item[u'user_id']) + ' написал: ' + recieved_str)
	@staticmethod
	def vk_auth():
		try:
			print('Viklund v.0.3')
			vk_login = input('Login:')
			vk_passwd = getpass.getpass('Password:')
			vk = vk_api.VkApi(login = vk_login, password = vk_passwd)
			vk.auth()
			vk_login = ''
			vk_passwd = ''
			return vk
		except vk_api.AuthError as error_msg:
			print(error_msg)
			exit(1)
		else:
			print('Auth successful')
