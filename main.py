import time
import vk_api
import random
import json
import os
import sys
import getpass
import viklund

def main():
	viklund.vk = viklund.Vk_system.vk_auth()
	viklund.Vk_system.ask_logs()
	values = {'out': 0,'count': 100,'time_offset': 60}
	tools = vk_api.VkTools(viklund.vk)
	viklund.vkApi = viklund.vk.get_api()
	while True:
	    response = viklund.vk.method('messages.get', values)
	    if response['items']:
	        values['last_message_id'] = response['items'][0]['id']
	    for item in response['items']:
	    	recieved_str = item[u'body'].lower()
	    	viklund.Vk_system.print_log(item, recieved_str, None)
	    	if recieved_str.find(u'лит') != -1 and recieved_str.find(u'рандом') != -1:
	    		rand = viklund.Vk_random()
	    		rand.set_toggle_random(True)
	    		status_code = viklund.rand.find_a_b(recieved_str)
	    		if status_code == -1:
	    			rand.abort_random(item, 0)
	    		elif status_code == 1:
	    			rand.set_result(rand.randint_wrapper(rand.get_a(), rand.get_b()))
	    			rand.success_random(item)
	    	elif recieved_str.find(u'лит') != -1 and recieved_str.find(u'пост') != -1:
	    		group_import = viklund.Vk_group_import()
	    		group_import.handle_import_request(item, recieved_str)
	    	recieved_str = u''
	    time.sleep(1)
if __name__ == "__main__":
	main()