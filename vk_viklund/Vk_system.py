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
	def success(message, return_message=False): #returning colored success message, gonna be useful for logging
		success_message = output_colors.BOLD + output_colors.OKGREEN + 'OK: ' + output_colors.ENDC + message
		if not return_message:
			print(success_message, file=sys.stderr)
		else:
			return success_message
	@staticmethod
	def warning(message, return_message=False): #returning colored warning message, gonna be useful for logging
		warning_message = output_colors.BOLD + output_colors.WARNING + 'WARNING: ' + output_colors.ENDC + message
		if not return_message:
			print(warning_message, file=sys.stderr)
		else:
			return warning_message
	@staticmethod
	def error(message, return_message=False): #returning colored error message, gonna be useful for logging
		error_message = output_colors.BOLD + output_colors.FAIL + 'ERROR: ' + output_colors.ENDC + message
		if not return_message:
			print(error_message, file=sys.stderr)
			exit(1)
		else: #exit will always work, nevertheless i'm using else
			return error_message

	@staticmethod
	def override_fd():
		dir = os.path.abspath(os.path.dirname(sys.argv[0])) #get absolute path to current dir (where the script is)
		log_dir = os.path.join(dir, 'vk_logs')
		try:
			os.mkdir(os.path.abspath(log_dir), 0o777)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = log_dir + '/viklund.log'
		log_file = None
		try:	
			log_file = open(file, 'x')
		except OSError:
			log_file = open(file, 'a')
		except Exception as e:
			viklund.Vk_system.error("unable to write to log file\n" + str(e))
		#we just override stdout and stderr file descriptors, it's more convenient
		file_fd = log_file.fileno()
		dup_fd = os.dup(file_fd)
		os.dup2(file_fd, sys.stdout.fileno())
		os.dup2(dup_fd, sys.stderr.fileno())
	@staticmethod
	def handle_args():
		arg_parser = argparse.ArgumentParser()
		arg_parser.add_argument ('-g', '--log', choices=['file', 'stdout',], default='file', type=str, action='store', help='select log type') #select logs output type
		arg_parser.add_argument('-l', '--login', nargs='?', type=str, action='store', help='input login, UNSAFE, USE CAREFULLY') #
		arg_parser.add_argument('-p', '--password', nargs='?', type=str, action='store', help='input password, UNSAFE, USE CAREFULLY')
		arg_parser.add_argument('-j', '--json_path', nargs='?', type=str, action='store', help='Path to .json file, needed for group post import, example: /path/to/file.json')
		args_namespace = arg_parser.parse_args(sys.argv[1:])
		if args_namespace.json_path:
			viklund.JSON_PATH = args_namespace.json_path
		log_file = None
		return args_namespace
	@staticmethod	
	def log_messages(item, received_str):
		#earlier, this function could track users' IDs and names
		#let's respect privacy
		output_str = 'Пользователь в ' + datetime.fromtimestamp(item['date']).strftime('%d/%m/%Y %H:%M:%S') + ' вызвал команду: ' + received_str
		viklund.Vk_system.echo_log(output_str)
	@staticmethod
	def echo_log(output_str, output_mode=None):
		additional_string = ''
		if output_mode != None:
			output_color = output_colors.HEADER + output_str + output_colors.ENDC #highlight important messages
			if output_mode == 'success':
				additional_string = output_colors.BOLD + output_colors.OKGREEN + 'OK: ' + output_colors.ENDC
			elif output_mode == 'warning':
				additional_string = output_colors.BOLD + output_colors.WARNING + 'WARNING: ' + output_colors.ENDC
			elif output_mode == 'error':
				additional_string = output_colors.BOLD + output_colors.FAIL + 'ERROR: ' + output_colors.ENDC
		time_now = '[' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '] '
		print(time_now + additional_string + output_str, file = sys.stderr)
		if output_mode == 'error':
			exit(0)
	@staticmethod
	def vk_auth(args_namespace):
			vk = None
			print('Viklund v.0.4')
			#if user haven't provided login as commandline argument, we'll ask him for this
			#otherwise, we'll just copy login from namespace variable to local variable
			if not args_namespace.login: 
				vk_login = input('Login:')
			else:
				vk_login = args_namespace.login
			#same for password
			if not args_namespace.password:
				vk_passwd = getpass.getpass('Password:')
			else:
				vk_passwd = args_namespace.password
			"""
			apparently most users may want to launch the bot in the terminal (e.g. ssh) and then close that shell
			but we don't want our process to be closed
			so we do auth procedure, clone process with fork() and kill the parent process
			even if user closes terminal, the process will be alive
			"""
			try:
				#get VK API access
				vk = vk_api.VkApi(login = vk_login, password = vk_passwd)
				vk.auth()
				del vk_login; del vk_passwd; del args_namespace #i think it's safer to delete import variables manually
			except vk_api.AuthError as error_msg:
				viklund.Vk_system.echo_log('Unable to log in. Please check that you have entered your login and password correctly.', output_mode='error')
			pid = os.fork()
			if pid: #parent process code goes here (pid > 0)
				viklund.Vk_system.echo_log('Auth successful, bot started with PID ' + str(pid), output_mode='success')
				viklund.Vk_system.override_fd()
				#output another to log file
				viklund.Vk_system.echo_log('Auth successful, bot started with PID ' + str(pid), output_mode='success')
				exit(0)
			else: #child process code goes here
				viklund.Vk_system.override_fd()	
				return vk