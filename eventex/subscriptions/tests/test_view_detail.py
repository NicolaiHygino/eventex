import hashlib
from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
	def setUp(self):
		email = 'nicolaihygino2000@gmail.com'
		hash_url = hashlib.md5(email.encode()).hexdigest()
		self.obj = Subscription.objects.create(
			name='Nicolai Hygino',
			cpf='12345678901',
			email=email,
			phone='21-982585168',
			hash_url=hash_url
		)
		self.resp = self.client.get(r('subscriptions:detail', self.obj.hash_url))

	def test_get(self):
		self.assertEqual(200, self.resp.status_code)

	def test_template(self):
		"""Must return subscriptions/subscriptions_detail.html"""
		self.assertTemplateUsed(self.resp, 
								'subscriptions/subscription_detail.html')

	def test_context(self):
		subscription = self.resp.context['subscription']
		self.assertIsInstance(subscription, Subscription)

	def test_hmtl(self):
		contents = (self.obj.name, self.obj.cpf, 
					self.obj.email, self.obj.phone)

		with self.subTest():
			for expected in contents:
				self.assertContains(self.resp, expected)


class SubscriptionDetailNotFound(TestCase):
	def test_not_found(self):
		resp = self.client.get(r('subscriptions:detail', 0))
		self.assertEqual(404, resp.status_code)