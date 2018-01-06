import viklund
import wikipedia
class Extra:
	@staticmethod
	def handle_wiki_search(search_request):
		wikipedia.set_lang("ru")
		try:
			search_result = wikipedia.summary(search_request)
			viklund.Message.send(message_text=search_result)
		except wikipedia.PageError:
			viklund.Message.send(message_text= '{}: not found'.format(search_request))
			raise
			return -1
		except:
			viklund.Message.send(message_text='An error occurred while searching')
			raise
	def handle_weather_request(request): #coming soon
		pass