from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r

class subscribePostValid(TestCase):
	def setUp(self):
		data = dict(name='Nicolai Hygino', cpf='12345678901',
					email='nicolaihygino2000@gmail.com', phone='21-98258-5168')
		self.client.post(r('subscriptions:new'), data)
		self.email = mail.outbox[0]


	def test_subscription_email_subject(self):
		expect = 'Confirmação de inscrição'

		self.assertEqual(expect, self.email.subject)


	def test_subscription_email_from(self):
		expect = 'contato@eventex.com.br'

		self.assertEqual(expect, self.email.from_email)


	def test_subscription_email_to(self):
		 expect = ['contato@eventex.com.br', 'nicolaihygino2000@gmail.com']

		 self.assertEqual(expect, self.email.to)


	def test_subscription_email_body(self):
		contents = [
			'Nicolai Hygino',
			'12345678901',
			'nicolaihygino2000@gmail.com',
			'21-98258-5168',
		]
		
		for content in contents:
			with self.subTest():
				self.assertIn(content, self.email.body)
		