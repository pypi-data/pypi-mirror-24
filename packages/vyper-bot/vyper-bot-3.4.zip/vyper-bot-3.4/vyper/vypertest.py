import pluginbot
import keyboard
import payments
import json
class VyperBot(pluginbot.PluginBot):
	def message(self, msg):
		msg = msg['message']
		self.test_plugins(msg)

	def callback_query(self, msg):
		print(msg)

	def pre_checkout_query(self, msg):
		msg = msg['pre_checkout_query']
		self.answerPreCheckoutQuery(msg['id'], True)

class Keyboard(pluginbot.Plugin):
	def message(self, msg):
		print('Testing keyboard')
		if msg['text'] == "/kb":
			print('Keyboard')
			kb = keyboard.Keyboard()
			kb.load_from_excel('keyboard.xls')
			self.bot.sendMessage(msg['chat']['id'], 'Inline keyboard test', reply_markup=kb.json)

stripe = '284685063:TEST:YWJkM2YyYzExOTY4'
pay = payments.Item('Test', 'Test', stripe, prices=[payments.LabeledPrice('Item', 500)])

class Pay(pluginbot.Plugin):
	def message(self, msg):
		print('Testing Payment')
		if msg['text'] == '/pay':
			print("PAYMENT")
			invoice, payload = pay.invoice(msg)
			self.bot.sendInvoice(*invoice)
			


if __name__ == "__main__":
	bot = VyperBot('402125473:AAEewgo3teZvpPc23gThnA0nVKqTPYuXq_0', start_loop=True, list_plugins=True)