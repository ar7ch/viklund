#Copyright (C) 2017 Artyom Bulgakov
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
import viklund
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