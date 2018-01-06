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
	def override_fd(log_file):
		"""
		Override stdout and stderr with opened logging file object log_file

		Parameters
		----------
			log_file
				Opened log file object.
		"""
		file_fd = log_file.fileno() #get file descriptor number of opened file
		dup_fd = os.dup(file_fd) #duplicate opened file for stderr
		os.dup2(file_fd, sys.stdout.fileno()) #stdout now will be redirected to our log file
		os.dup2(dup_fd, sys.stderr.fileno()) #stderr now will be redirected to our log file

	@staticmethod
	def initialize_logs():
		"""
		Initialize log folder and log file.

		Create directory for logging file and logging file (or check if it exists) and return opened file object

		Returns
		-------
		file
			Opened log file object
		"""
		dir_name = 'viklund-logs'
		file_name = 'viklund.log'
		dir_path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), dir_name) #get abs path to logging directory
		try:
			os.mkdir(os.path.abspath(dir_path), 0o777)
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file_path = os.path.join(dir_path, file_name); #join file name to logging directory path
		log_file = None
		try:	
			log_file = open(file_path, 'x') #try to create file
		except OSError: #if file already exists
			log_file = open(file_path, 'a') #append to file
		except Exception as e: #something else bad happened
			print(viklund.Logging.error(str(e)))
			exit(1)
		return log_file

	@staticmethod	
	def log_messages(item):
		"""
		Get date of recieved message, and return formatted string with timedate prefix for logging output

		Parameters
		----------
			item
				Item section of response.
		Returns
			output_str : string
				Formatted string with timedate prefix
		"""
		format_type = '%d/%m/%Y %H:%M:%S'
		date = datetime.fromtimestamp(item['date']).strftime(format_type)
		output_str = 'Пользователь в ' + date + ' вызвал команду: ' + item['body']
		return output_str

	@staticmethod
	def success(success_message):
		"""
		Return success_message string with green OK prefix.

		Parameters
		----------
			success_message : string
				Success message.
		
		Returns
		-------
			: string
				Success_message string with green OK prefix.

		"""
		return Logging.BOLD + Logging.OKGREEN + 'OK: ' + Logging.ENDC + str(success_message) + '\n'

	@staticmethod
	def warning(warning_message):
		"""
		Return warning_message string with yellow WARNING prefix.

		Parameters
		----------
			warning_message : string
				Warning message.
		
		Returns
		-------
			: string
				warning_message string with yellow WARNING prefix.

		"""
		return Logging.BOLD + Logging.WARNING + 'WARNING: ' + Logging.ENDC + str(warning_message) + '\n'

	@staticmethod
	def error(error_message):
		"""
		Return error_message string with red ERROR prefix.

		Parameters
		----------
			error_message : string
				Error message.
		
		Returns
		-------
			: string
				Error_message string with red ERROR prefix.

		"""
		return Logging.BOLD + Logging.FAIL + 'ERROR: ' + Logging.ENDC + str(error_message) + '\n'

	@staticmethod
	def write_log(output_str):
		"""
		Write output_str to log file with timedate prefox.

		Parameters
		----------
			output_str
				Formatted string with timedate prefix.
		"""
		date_format = '%Y-%m-%d %H:%M:%S'
		date_now = datetime.now().strftime(date_format)
		time_now = '[ {} ] '.format(date_now)
		print(time_now + output_str, file = sys.stderr)
