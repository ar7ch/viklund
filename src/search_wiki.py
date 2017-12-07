import viklund
import wikipedia

@staticmethod
	def handle_wiki_search_request(item, received_str):
		search_request = received_str[5:] # skip /вики characters
		wikipedia.set_lang("ru")
		try:
			search_result = wikipedia.summary(search_request)
			viklund.Vk_messages.send_selective(item, 'msg', search_result)
		except wikipedia.PageError as ex:
			viklund.Vk_messages.send_selective(item, 'msg', search_request + ': страница не найдена')
			viklund.Vk_system.echo_log(str(ex), output_mode='warning')
			return -1
		except wikipedia.UserWarning as warning:
			viklund.Vk_system.echo_log(str(warning), output_mode='warning')
		except:
			viklund.Vk_messages.send_selective(item, 'msg', 'Произошла ошибка во время поиска')
