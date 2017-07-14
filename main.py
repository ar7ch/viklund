import viklund

def main():
	viklund.vk = viklund.Vk_system.vk_auth()
	viklund.Vk_system.ask_logs()
	viklund.vkApi = viklund.vk.get_api()
	viklund.Vk_messages.handle_messages()
if __name__ == "__main__":
	main()