import os
import requests
import pystyle


class WebhookHandler:
	def __init__(self, webhook: str, message: str, amount: int = 99999999, ping: int = 1):
		self.webhook = webhook
		self.message = message
		self.amount  = amount
		
		# 1 = @everyone 2 = @here 3 = None
		if ping == 1:
			self.ping = '@everyone'
		elif ping == 2:
			self.ping = '@here'
		elif ping == 3:
			self.ping = False
		else:
			raise ValueError("Unknown Value for ping!")
		
		if not self.is_webhook_valid(webhook=self.webhook):
			print("[-] Webhook entered is not an valid webhook! Was it deleted?")
			exit()
	
	@staticmethod
	def is_webhook_valid(webhook: str):
		r = requests.get(webhook)
		if r.status_code == 200:
			return True
		return False
	
	def spam_webhook(self):
		payload = {
			'avatar_url': 'https://cdn.discordapp.com/attachments/1138965240227311727/1138967959520420000/logo.png',
			'username': 'Fucked with Diamond Back',
			'content': self.message + f' {self.ping if self.ping else ""} '
		}
		sent = 1
		for i in range(int(self.amount)):
			try:
				r = requests.post(self.webhook, json=payload)
				if r.status_code == 204 or r.status_code == 200:
					print(f'\r[+] Message Sent {sent}x', end='')
					sent += 1
			except Exception:
				print('[-] Webhook is dead')
				break
			except KeyboardInterrupt:
				print('\n[!] Exiting..')
				return True
	
	def delete_webhook(self):
		try:
			r = requests.delete(self.webhook)
			if r.status_code == 204 or r.status_code == 200:
				print('[+] Deleted Webhook')
		except Exception:
			print('[-] Webhook is dead')


class Menu:
	def __init__(self):
		self.LOGO = """ /$$$$$$$  /$$                                                   /$$       /$$$$$$$                      /$$
| $$__  $$|__/                                                  | $$      | $$__  $$                    | $$
| $$  \ $$ /$$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$  /$$$$$$$   /$$$$$$$      | $$  \ $$  /$$$$$$   /$$$$$$$| $$   /$$
| $$  | $$| $$ |____  $$| $$_  $$_  $$ /$$__  $$| $$__  $$ /$$__  $$      | $$$$$$$  |____  $$ /$$_____/| $$  /$$/
| $$  | $$| $$  /$$$$$$$| $$ \ $$ \ $$| $$  \ $$| $$  \ $$| $$  | $$      | $$__  $$  /$$$$$$$| $$      | $$$$$$/
| $$  | $$| $$ /$$__  $$| $$ | $$ | $$| $$  | $$| $$  | $$| $$  | $$      | $$  \ $$ /$$__  $$| $$      | $$_  $$
| $$$$$$$/| $$|  $$$$$$$| $$ | $$ | $$|  $$$$$$/| $$  | $$|  $$$$$$$      | $$$$$$$/|  $$$$$$$|  $$$$$$$| $$ \  $$
|_______/ |__/ \_______/|__/ |__/ |__/ \______/ |__/  |__/ \_______/      |_______/  \_______/ \_______/|__/  \__/"""
		
		self.menu()
	
	def menu(self, webhook: str = None):
		print(pystyle.Colorate.Vertical(pystyle.Colors.blue_to_cyan, self.LOGO))
		
		print('-' * 114)
		
		options = ['Spam Webhook', 'Delete Webhook', "Exit"]
		ping_ops = ['@everyone', '@here', 'none']
		
		for i, option in enumerate(options):
			print(f"[{i + 1}] {option}")
		
		action = input("Enter Choice >> ")
		
		try:
			action = int(action)
		except ValueError:
			print("Invalid Option.")
			exit()
		
		if action - 1 == 2:
			exit()
		else:
			if webhook is None:
				webhook = input("Webhook URL: ")
		
		if not webhook or not webhook.startswith('https://') or not webhook.startswith('http://'):
			print('[-] Please enter a webhook!')
			exit()
		
		if action - 1 == 1:
			webh = WebhookHandler(webhook=webhook, message='hi')
			webh.delete_webhook()
		else:
			message = input("Message (DO NOT INCLUDE PING): ")
			for i, option in enumerate(ping_ops):
				print(f"[{i+1}] {option}")
			
			ping = input("Enter Ping Choice >> ")
			
			try:
				ping = int(ping)
			except ValueError:
				exit("Invalid Ping Option.")
			
			webh = WebhookHandler(webhook=webhook, message=message, ping=ping)
			exited = webh.spam_webhook()
			os.system("cls" if os.name == 'nt' else 'clear')
			self.menu(webhook)


if __name__ == "__main__":
	m = Menu()
