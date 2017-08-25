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

import vk_api
import random
import json
import os
import errno
import sys
import getpass
import viklund
import argparse
from datetime import datetime

class output_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Vk_system():
	@staticmethod
	def handle_args():
		arg_parser = argparse.ArgumentParser()
		arg_parser.add_argument ('-g', '--log', choices=['file', 'stdout',], default='file', type=str, action='store', help='select log type') #select logs output type
		arg_parser.add_argument('-l', '--login', nargs='?', type=str, action='store', help='input login, UNSAFE, USE CAREFULLY') #
		arg_parser.add_argument('-p', '--password', nargs='?', type=str, action='store', help='input password, UNSAFE, USE CAREFULLY')
		arg_parser.parse_args(sys.argv[1:])
		return arg_parser

	@staticmethod
	def print_log(item, recieved_str, type):
		if viklund.logs_policy == 1:
			pathname = os.path.abspath(os.path.dirname(sys.argv[0])) #get absolute path to current dir (where the script is)
			pathname = os.path.join(pathname, 'vk_logs')
			log_file = None
			try:	
				log_file = open(log_location, 'x')
			except OSError:
				log_file = open(log_location, 'a')
			finally:
				viklund.Vk_system.log_messages(item, log_file, recieved_str)
				log_file.close()
		elif viklund.logs_policy == 'stdout':
			viklund.Vk_system.log_messages(item, None, recieved_str)
	@staticmethod
	def log_messages(item, log_file, recieved_str):
		if viklund.logs_policy == 1 or viklund.logs_policy == 2:
			user = viklund.vkApi.users.get(user_ids=item[u'user_id'])
			username = user[0]['first_name'] + ' ' + user[0]['last_name'] + ' '
			user = None
			if viklund.Vk_messages.check_if_chat(item):
				output_str = username + '(' + 'id ' + str(item[u'user_id']) + ') ' + 'в беседе с id ' + str(item[u'chat_id']) + ' в ' + datetime.fromtimestamp(item['date']).strftime('%d/%m/%Y %H:%M:%S') + ': ' + recieved_str
				viklund.Vk_system.log_selective(item, log_file, output_str)
			else:
				output_str = username + '(' + 'id ' + str(item[u'user_id']) + ') ' + 'в личном сообщении в ' + datetime.fromtimestamp(item['date']).strftime('%H:%M:%S %d/%m/%Y') + ': ' + recieved_str
				viklund.Vk_system.log_selective(item, None, output_str)
	@staticmethod
	def log_selective(item, log_file, output_str):
		if viklund.logs_policy == 1 or viklund.logs_policy == 2:
			time_now = '[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] '
			if viklund.logs_policy == 1:
				log_file.write(time_now + output_str + '\n')
			elif viklund.logs_policy == 2:
				print(time_now + output_str)
	@staticmethod
	def vk_auth(args):
		try:
			print('Viklund v.0.4')
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
		finally:
			print('Auth successful')
