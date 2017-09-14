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

import viklund
import time
import os, sys
from datetime import datetime

def handle_messages():
	values = {'out': 0,'count': 100,'time_offset': 60}
	while True:
		try:
			response = viklund.vk.method('messages.get', values)
			if response['items']:
				values['last_message_id'] = response['items'][0]['id']
			for item in response['items']:
				#your user messages handling code starts here
				received_str = item[u'body'].lower()
				#handle messages that only begin with slash
			if len(received_str) > 1 and received_str[0] == '/':
				viklund.Vk_system.log_messages(item, received_str)
				if received_str.find(u'рандом') != -1:
					viklund.Vk_random.handle_random(item, received_str)
				elif received_str.find(u'пост') != -1:
					viklund.Vk_group_import.handle_import_request(item, received_str, JSON_PATH)
				elif received_str.find(u'перешли') != -1:
					viklund.Vk_messages.resend_user_message(item, received_str)
				elif received_str.find(u'айди') != -1:
					viklund.Vk_messages.handle_id_request(item)
				elif received_str.find(u'вики') != -1:
					viklund.Vk_messages.handle_wiki_search_request(item, received_str)
				elif received_str.find(u'помощь') != -1:
					viklund.Vk_messages.send_selective(item, 'msg', 'Viklund Bot\nИспользование: \'/команда\'\nДоступные команды:\nпост\nрандом\nперешли\nайди\nпомощь')
				#hidden feature
				elif received_str.find(u'статус') != -1:
					viklund.Vk_messages.send_selective(item, 'msg', 'Viklund v.0.4\nСтатус: up\nВремя на сервере: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
				else:
					viklund.Vk_messages.send_selective(item, 'msg', received_str[1:] + ': команда не найдена')
				received_str = u''
		except Exception as e:
			viklund.Vk_system.echo_log(str(e), output_mode='warning')
		time.sleep(1)

def main():
	args = viklund.Vk_system.handle_args();
	viklund.vk = viklund.Vk_system.vk_auth(args)
	viklund.vkApi = viklund.vk.get_api()
	handle_messages()
if __name__ == "__main__":
	main()