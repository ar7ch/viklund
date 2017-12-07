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

class Logging():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
	def override_fd(log_fd):
		"""override stdout and stderr with opened logging file descriptor log_fd"""
		file_fd = log_fd.fileno() #get file descriptor number of opened file
		dup_fd = os.dup(file_fd) #duplicate opened file for stderr
		os.dup2(file_fd, sys.stdout.fileno()) #stdout now will be redirected to our log file
		os.dup2(dup_fd, sys.stderr.fileno()) #stderr now will be redirected to our log file

    @staticmethod
    def initialize_logs():
    	"""create directory for logging file and logging file (or check if it exists) and return opened file object"""
    	dir_name = 'viklund-logs'
		file_name = 'viklund.log'
		dir_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), dir_name) #get abs path to logging directory
		try:
			os.mkdir(os.path.abspath(log_dir), 0o777)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file_path = os.path.join(log_dir_path, file_name); #join file name to logging directory path
		log_file = None
		try:	
			log_file = open(file, 'x') #try to create file
		except OSError: #if file already exists
			log_file = open(file, 'a') #append to file
		except Exception as e: #something else bad happened
			viklund.Vk_system.error("unable to write to log file\n" + str(e))
		return log_file

	@staticmethod	
	def message_log_str(item, received_str):
		"""get date of recieved message, and return formatted string for logging output"""
		format_type = '%d/%m/%Y %H:%M:%S'
		date = datetime.fromtimestamp(item['date']).strftime(format_type)
		output_str = 'Пользователь в ' + date + ' вызвал команду: ' + received_str
		return output_str

	@staticmethod
	def success(success_message):
		return Logging.BOLD + Logging.OKGREEN + 'OK: ' + Logging.ENDC + success_message + '\n'

	@staticmethod
	def warning(warning_message):
		return Logging.BOLD + Logging.WARNING + 'WARNING: ' + Logging.ENDC + warning_message + '\n'

	@staticmethod
	def error(error_message):
		return Logging.BOLD + Logging.FAIL + 'ERROR: ' + Logging.ENDC + '\n'

	@staticmethod
	def write_log(output_str):
		"""write string output_str to log file"""
		date_format = '%Y-%m-%d %H:%M:%S'
		date_now = datetime.now().strftime(date_format)
		time_now = '[' + date_now + '] '
		print(time_now + additional_string + output_str, file = sys.stderr)

class System():
	@staticmethod
	def setup():
		args = viklund.System.handle_args();
		viklund.vk = viklund.Vk_system.auth(args)
		viklund.vkApi = viklund.vk.get_api()
		"""
		apparently most users may want to launch the bot in the terminal (e.g. ssh) and then close that shell
		but we don't want our process to be closed
		so we do auth procedure, clone process with fork() and kill the parent process
		even if user closes terminal, the process will be alive
		"""
		pid = os.fork()
		if pid: #parent process code goes here (pid > 0)
			viklund.Vk_system.echo_log('Auth successful, bot started with PID ' + str(pid), output_mode='success')
			viklund.Vk_system.override_fd()
			#output another to log file
			viklund.Vk_system.echo_log('Auth successful, bot started with PID ' + str(pid), output_mode='success')
			exit(0)
		else: #child process code goes here
			viklund.Vk_system.override_fd()	
	@staticmethod
	def handle_args():
		arg_parser = argparse.ArgumentParser()
		arg_parser.add_argument('-g', '--log', choices=['file', 'stdout',], default='file', type=str, action='store', help='select log type') #select logs output type
		arg_parser.add_argument('-l', '--login', nargs='?', type=str, action='store', help='input login, UNSAFE, USE CAREFULLY') #
		arg_parser.add_argument('-p', '--password', nargs='?', type=str, action='store', help='input password, UNSAFE, USE CAREFULLY')
		arg_parser.add_argument('-j', '--json_path', nargs='?', type=str, action='store', help='Path to .json file, needed for group post import, example: /path/to/file.json')
		args_namespace = arg_parser.parse_args(sys.argv[1:])
		if args_namespace.json_path:
			viklund.JSON_PATH = args_namespace.json_path
		else:
			viklund.JSON_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/default.json'
		log_file = None
		return args_namespace

	@staticmethod
	def auth(args_namespace):
		vk = None
		print('Viklund v.0.5')
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
		try:
			#get VK API access
			vk = vk_api.VkApi(login = vk_login, password = vk_passwd)
			vk.auth()
			del vk_login; del vk_passwd; del args_namespace #it should be safer to delete import variables manually
		except vk_api.AuthError as error_msg:
			viklund.Logging.write_log(Logging.error('Unable to log in. Please check that you have entered your login and password correctly.'))
			os.exit(1)
		else:
			viklund.Logging.write_log(Logging.success("Auth successful"))
		return vk