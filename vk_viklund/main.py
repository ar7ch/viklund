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

JSON_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) 
def handle_messages():
	values = {'out': 0,'count': 100,'time_offset': 60}
	while True:
		response = viklund.vk.method('messages.get', values)
		if response['items']:
			values['last_message_id'] = response['items'][0]['id']
		for item in response['items']:
			#ваш код для обработки сообщений пользователей начинается здесь
			recieved_str = item[u'body'].lower()
			viklund.Vk_system.print_log(item, recieved_str, None)
			try:
				if len(recieved_str) > 1 and recieved_str[0] == '/': #синтаксис команд: /command
					if recieved_str.find(u'рандом') != -1:
						viklund.Vk_random.handle_random(item, recieved_str)
					elif recieved_str.find(u'пост') != -1:
						viklund.Vk_group_import.handle_import_request(item, recieved_str, JSON_PATH)
					elif recieved_str.find(u'перешли') != -1:
						viklund.Vk_messages.resend_user_message(item, recieved_str)
					elif recieved_str.find(u'айди') != -1:
						viklund.Vk_messages.handle_id_request(item)
					elif recieved_str.find(u'помощь') != -1:
						viklund.Vk_messages.send_selective(item, 'msg', 'Viklund Bot\nИспользование: \'/команда\'\nДоступные команды:\nпост\nрандом\nперешли\nайди\nпомощь')
					else:
						viklund.Vk_messages.send_selective(item, 'msg', recieved_str[1:] + ': команда не найдена')
					recieved_str = u''
			except Exception as e:
				print(e)
		time.sleep(1)

def main():
	viklund.vk = viklund.Vk_system.vk_auth()
	viklund.Vk_system.ask_logs()
	viklund.vkApi = viklund.vk.get_api()
	handle_messages()
if __name__ == "__main__":
	main()