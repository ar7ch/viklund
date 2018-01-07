#/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Copyright (C) 2017-2018 Artyom Bulgakov

This file is part of viklund.
Viklund is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
Viklund is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with viklund.  If not, see <http://www.gnu.org/licenses/>.
"""

import vk_api
import os
import errno
import sys
import getpass
import viklund
import argparse
from datetime import datetime
import traceback

class System():
	@staticmethod
	def setup():
		"""
		step 1: parse args
		step 2: auth 
		step 3: create log folder and file
		step 4:	duplicate current process 
		step 5: override file descriptors to output logs to file
		step 6: get api access
		"""
		args = viklund.System.handle_args();
		viklund.vk_session = viklund.System.auth(args)
		log_file = viklund.Logging.initialize_logs()
		"""
		apparently most users may want to launch the bot in the terminal (e.g. ssh) and then close that terminal sessions
		but we don't want our process to be closed
		so we do auth procedure, clone process with fork() and exit the parent process
		even if user closes terminal, the bot process will be alive
		"""
		pid = os.fork()
		if pid: #parent process code goes here (pid > 0)
			#parent only shows success message and exits
			success_message = viklund.Logging.success('Bot started with PID ' + str(pid))
			viklund.Logging.write_log(success_message) #output to terminal
			viklund.Logging.override_fd(log_file)
			viklund.Logging.write_log(success_message) #output to log file
			exit(0)
		else: #child process code goes here
			viklund.vkApi = viklund.vk_session.get_api()
			viklund.Logging.override_fd(log_file)
	@staticmethod
	def handle_args():
		"""
		Handle arguments.

		Returns
		-------
			args_namespace
				Arguments namespace.
		"""
		arg_parser = argparse.ArgumentParser()
		arg_parser.add_argument('-l', '--login', nargs='?', type=str, action='store', help='pass login via commandline, UNSAFE, USE CAREFULLY') #
		arg_parser.add_argument('-p', '--password', nargs='?', type=str, action='store', help='pass password via commandline, UNSAFE, USE CAREFULLY')
		
		arg_parser.add_argument('-i', '--input_token', nargs='?', type=str, action='store', help='Pass token via commandline, UNSAFE, USE CAREFULLY')
		arg_parser.add_argument('-t', '--token', action='store_const', const=True, help='make Viklund wait for input a token, not login and password')
		
		arg_parser.add_argument('-j', '--json_path', nargs='?', type=str, action='store', help='Path to .json file, needed for group post import, example: /path/to/file.json')
		arg_parser.add_argument('-g', '--log_path', nargs='?', type=str, action='store', help='Path where logs directory should be created')
		
		args_namespace = arg_parser.parse_args(sys.argv[1:])
		if args_namespace.json_path:
			viklund.JSON_PATH = args_namespace.json_path
		else:
			viklund.JSON_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/default.json'
		if args_namespace.log_path:
			viklund.LOGS_PATH = args_namespace.log_path
		return args_namespace

	@staticmethod
	def auth(args_namespace):
		"""
		Auth to VK and return active VK session.

		Parameters
		----------
			args_namespace
				Arguments namespace returned by handle_args()
		Raises
		------
			AuthError
				Authentication error.
		"""
		vk_session = None
		vk_token = None
		vk_login = None
		vk_passwd = None
		print('Viklund v.0.6')
		#if user haven't provided login as commandline argument, ask him for login
		#otherwise, we'll just copy login from namespace variable to local variable
		if not args_namespace.login:
			if args_namespace.input_token:
				vk_token = args_namespace.input_token
			elif args_namespace.token:
				vk_token = input('Token:')
			else:
				vk_login = input('Login:')
		if args_namespace.login:
			vk_login = args_namespace.login
		#same for password
		if not args_namespace.password:
			if not vk_token:
				vk_passwd = getpass.getpass('Password:')
		elif args_namespace.password:
			vk_passwd = args_namespace.password
		try:
			#get VK API access
			if vk_token:
				vk_session = viklund.vk_api.VkApi(token = vk_token)
			else:
				vk_session = viklund.vk_api.VkApi(login = vk_login, password = vk_passwd)
			vk_session.auth()
			del vk_login; del vk_passwd; del args_namespace #it might be safer to delete import variables manually
		except vk_api.AuthError as error_msg:
			print(viklund.Logging.error('Unable to log in. Please check that you have entered your login and password correctly.'))
			exit(1)
		else:
			viklund.Logging.write_log(viklund.Logging.success("Auth successful"))
		return vk_session