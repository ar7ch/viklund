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

import viklund
import wikipedia
from googletrans import Translator

class Extra:
	@staticmethod
	def handle_translate_request(translate_request, arguments):
		"""
		Translate text using googletrans module.
		Parameters
		-----------
			translate_request : string
				String to translate
			arguments : str list
				List of arguments. arguments[0] is source language code, arguments[1] is destination language code.
		Raises
		-------
			ValueError
				If got invalid language code.
			Exception
				Other errors occured.
		"""
		try:
			translator = Translator()
			source_lang = None
			dest_lang = None
			if not translate_request:
				viklund.Message.send(message_text='Нечего переводить')
			if arguments:
				
				if len(arguments) == 2:
					source_lang = arguments[0][1:]
					dest_lang = arguments[1][1:]
					translation = translator.translate(translate_request, dest=dest_lang, src=source_lang)
				else:
					viklund.Message.send(message_text='Пожалуйста, укажите два аргумента (начинающихся со -): код исходного языка и код языка назначения.')
					return
			else:
				detection = translator.detect(translate_request)
				source_lang = detection.lang
				if source_lang != 'ru':
					dest_lang = 'ru'
					translation = translator.translate(translate_request, dest=dest_lang)
				elif source_lang == 'ru':
					dest_lang = 'en'
					translation = translator.translate(translate_request, dest=dest_lang)
				else:
					viklund.Message.send(viklund.Message.send(message_text='Unable to detect language'))
					return
			viklund.Message.send(message_text='''Переведено!\nИсходный язык: {0}\nЯзык назначения: {1}'''.format(source_lang, dest_lang))
			viklund.Message.send(message_text = translation.text)
		except ValueError:
			viklund.Message.send(message_text='''
				Неверный код языка!
				Доступные коды:
				af Африкаанс 
				am Амхарский 
				ar Арабский 
				az Азербайджанский 
				ba Башкирский 
				be Белорусский 
				bg Болгарский 
				bn Бенгальский 
				bs Боснийский 
				ca Каталанский 
				ceb Себуанский 
				cs Чешский 
				cy Валлийский 
				da Датский 
				de Немецкий 
				el Греческий 
				en Английский 
				eo Эсперанто 
				es Испанский 
				et Эстонский 
				eu Баскский 
				fa Персидский 
				fi Финский 
				fr Французский 
				ga Ирландский 
				gd Шотландский (гэльский) 
				gl Галисийский 
				gu Гуджарати 
				he Иврит 
				hi Хинди 
				hr Хорватский 
				ht Гаитянский 
				hu Венгерский 
				hy Армянский 
				id Индонезийский 
				is Исландский 
				it Итальянский 
				ja Японский 
				jv Яванский 
				ka Грузинский 
				kk Казахский 
				kn Каннада 
				ko Корейский 
				ky Киргизский 
				la Латынь 
				lb Люксембургский 
				lt Литовский 
				lv Латышский 
				mg Малагасийский 
				mhr Марийский 
				mi Маори 
				mk Македонский 
				ml Малаялам 
				mn Монгольский 
				mr Маратхи 
				mrj Горномарийский 
				ms Малайский 
				mt Мальтийский 
				ne Непальский 
				nl Голландский 
				no Норвежский 
				pa Панджаби 
				pap Папьяменто 
				pl Польский 
				pt Португальский 
				ro Румынский 
				ru Русский 
				si Сингальский 
				sk Словацкий 
				sl Словенский 
				sq Албанский 
				sr Сербский 
				su Сунданский 
				sv Шведский 
				sw Суахили 
				ta Тамильский 
				te Телугу 
				tg Таджикский 
				th Тайский 
				tl Тагальский 
				tr Турецкий 
				tt Татарский 
				udm Удмуртский 
				uk Украинский 
				ur Урду 
				uz Узбекский 
				vi Вьетнамский 
				xh Коса 
				yi Идиш 
				zh Китайский
				''')
			raise
			return
		except Exception:
			raise
			return

	@staticmethod
	def handle_wiki_search(search_request):
		"""
		Search for request on Wikipedia.

		Parameters
		----------
		search_request : string 
			Request to find.
		
		Raises
		______
			wikipedia.PageError:
				If page doesn't exist
			wikipedia.DisambiguationError
				If page is a disambiguation page.
			Exception
				Other possible errors.
		"""
		wikipedia.set_lang("ru")
		try:
			search_result = wikipedia.summary(search_request)
			viklund.Message.send(message_text=search_result)
		except wikipedia.PageError:
			viklund.Message.send(message_text= '{}: не найдено'.format(search_request))
			return
		except wikipedia.DisambiguationError as e:
			viklund.Message.send(message_text=str(e))
			return
		except:
			viklund.Message.send(message_text='Произошла ошибка во время поиска')
			return
	def handle_weather_request(request): #coming soon
		pass