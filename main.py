import viklund

def handle_messages():
	values = {'out': 0,'count': 100,'time_offset': 60}
	while True:
		response = viklund.vk.method('messages.get', values)
		if response['items']:
			values['last_message_id'] = response['items'][0]['id']
		for item in response['items']:
			recieved_str = item[u'body'].lower()
			viklund.Vk_system.print_log(item, recieved_str, None)
			if recieved_str.find(u'лит') != -1 and recieved_str.find(u'рандом') != -1:
				viklund.Vk_random.handle_random(item, recieved_str)
			elif recieved_str.find(u'лит') != -1 and recieved_str.find(u'пост') != -1:
				viklund.Vk_group_import.handle_import_request(item, recieved_str)
			elif recieved_str.find(u'лит') != -1 and recieved_str.find(u'перешли') != -1:
				viklund.Vk_messages.resend_user_message(item, recieved_str)
			elif recieved_str.find(u'лит') != -1 and recieved_str.find(u'айди') != -1:
				viklund.Vk_messages.handle_id_request(item)
		recieved_str = u''
		time.sleep(1)

def main():
	viklund.vk = viklund.Vk_system.vk_auth()
	viklund.Vk_system.ask_logs()
	viklund.vkApi = viklund.vk.get_api()
	handle_messages()
if __name__ == "__main__":
	main()