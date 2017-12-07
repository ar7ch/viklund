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


import random
import viklund

class viklund_random:
	@staticmethod
	def handle_random(item, received_str):
		rand = viklund.Vk_random()
		rand.set_toggle_random(True)
		try:
			status_code = rand.parse_numbers(received_str)
			if status_code == -1:
				raise
		except:
			viklund.Vk_messages.send_selective(item, 'msg', u'Что-то пошло не так. Убедитесь, что вы ввели оба числа.')
			return -1
		else:
			rand.set_result(rand.get_random_number(rand.get_a(), rand.get_b()))
			viklund.Vk_messages.send_selective(item, 'msg', u'Успешно! Ваше случайное число в диапазоне от ' + str(min(self.get_a(), self.get_b())) + u' до ' + str(max(self.get_a(), self.get_b())) + u': ' + str(self.get_result()))
	def parse_numbers(self, received_str):
		self.set_a('')
		self.set_b('') 
		counter = 0
		for symbol in received_str:
			if '1234567890'.find(symbol) != -1:
				counter += 1
		if counter < 2:
			return -1
		else:
			got_a_flag = False
			got_b_flag = False
			digit_flag = False
			for symbol in received_str:
				if symbol.isdigit() and not got_a_flag and not got_b_flag:
					digit_flag = True
					self.set_a(self.get_a() + symbol)
				elif symbol.isdigit() and digit_flag and not got_a_flag and not got_b_flag:
					self.set_a(self.get_a() + symbol)
				elif not symbol.isdigit() and digit_flag and not got_a_flag and not got_b_flag:
					digit_flag = False
					got_a_flag = True
				elif symbol.isdigit() and not digit_flag and got_a_flag and not got_b_flag:
					digit_flag = True
					self.set_b(self.get_b() + symbol)
				elif symbol.isdigit() and digit_flag and not got_b_flag and got_a_flag:
					self.set_b(self.get_b() + symbol)
				elif not symbol.isdigit() and digit_flag and not got_b_flag and got_a_flag:
					digit_flag = False
					got_b_flag = True
					self.set_a(int(self.get_a))
					self.set_b(int(self.get_b))
					return 1
		return -1

	def get_random_number(self, a, b):
		a = int(a)
		b = int(b)
		return random.randint(min(a,b), max(a,b))
	def set_a(self, value):	
		self.a = value
	def get_a(self):
		return self.a
	def set_b(self, value):
		self.b = value
	def get_b(self):
		return self.b
	def __init__(self):
		pass
	a = None
	b = None
