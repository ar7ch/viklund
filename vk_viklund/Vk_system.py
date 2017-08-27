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
	def error(message):
		print(output_colors.BOLD + output_colors.FAIL + 'ERROR: ' + output_colors.ENDC + message, file=sys.stderr)
		exit(1)
	@staticmethod
	def handle_args():
		arg_parser = argparse.ArgumentParser()
		arg_parser.add_argument ('-g', '--log', choices=['file', 'stdout',], default='file', type=str, action='store', help='select log type') #select logs output type
		arg_parser.add_argument('-l', '--login', nargs='?', type=str, action='store', help='input login, UNSAFE, USE CAREFULLY') #
		arg_parser.add_argument('-p', '--password', nargs='?', type=str, action='store', help='input password, UNSAFE, USE CAREFULLY')
		args_namespace = arg_parser.parse_args(sys.argv[1:])
		pathname = os.path.abspath(os.path.dirname(sys.argv[0])) #get absolute path to current dir (where the script is)
		pathname = os.path.join(pathname, 'vk_logs')
		log_file = None
		try:	
			log_file = open(log_location, 'x')
		except OSError.FileExistsError:
			log_fd = open(log_location, 'a')
		except Exception as e:
			viklund.Vk_system.error("unable to write to log file\n" + e)
		#we just override stdout and stderr file descriptors, it's more convenient
		file_fd = log_file.fileno()
		dup_fd = os.dup(file_fd)
		os.dup2(file_fd, sys.stdout.fileno())
		os.dup2(dup_fd, sys.stderr.fileno())
		return args_namespace
	@staticmethod	
	def log_messages(recieved_str):
		#earlier, this function could track users' IDs and names
		#let's respect privacy
		output_str = 'Пользователь в ' + datetime.fromtimestamp(item['date']).strftime('%d/%m/%Y %H:%M:%S') + ' вызвал команду: ' + recieved_str
		log_messages(output_str)
	@staticmethod
	def log_selective(item, log_file, output_str):
		time_now = '[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] '
			print(time_now + output_str)
	@staticmethod
	def vk_auth(args_namespace):
			"""
			apparently most users may want to launch the bot in the terminal (e.g. ssh) and then close that shell
			but we don't want our process to be closed
			so we do auth procedure, clone process with fork() and kill the parent process
			even if user closes terminal, the process will be alive
			"""
			pid = os.fork()
			if pid: #parent process code goes here (pid > 0)
				print('Viklund v.0.4')
				vk_login = ''
				vk_passwd = ''
				try:
					#if user haven't provided login as commandline argument, we'll ask him for this
					#otherwise, we'll just copy login from namespace variable to local variable
					if not args_namespace.login: 
						vk_login = input('Login:')
					else
						vk_login = args_namespace.login
					#same for password
					if not args_namespace.password:
						vk_passwd = getpass.getpass('Password:')
					else
						vk_passwd = args_namespace.password
					vk = vk_api.VkApi(login = vk_login, password = vk_passwd)
					vk.auth()
					del vk_login; del vk_passwd; del args_namespace #i think it's safer to delete import variables manually
					viklund.vk = vk
					exit(0)
					print('Auth successful, bot started with PID is ' + str(pid))
				except vk_api.AuthError as error_msg:
					print(error_msg)
					exit(1)
