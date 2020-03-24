import hashlib
from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):
	def setUp(self):
		self.resp = self.client.get(r('subscriptions:new'))

	def test_get(self):
		"""Get /inscricao/ must returns status code 200"""

		self.assertEqual(200, self.resp.status_code)

	def test_template(self):
		"""Must use subscriptions/subscription_form.html"""
		self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

	def test_html(self):
		"""Html must countain input tags"""
		tags = (('<form', 1),
				('<input', 6),
				('type="text"', 3),
				('type="email"', 1),
				('type="submit"', 1))

		for text, count in tags:
			with self.subTest():
				self.assertContains(self.resp, text, count)

	def test_csrf(self):
		"""Html must countain csrf"""
		self.assertContains(self.resp, 'csrfmiddlewaretoken')

	def test_has_form(self):
		"""Content must have subscriprion form"""
		form  = self.resp.context['form']
		self.assertIsInstance(form, SubscriptionForm)


class SubscriptionsNewPostValid(TestCase):
	def setUp(self):
		self.data = dict(name='Nicolai Hygino', cpf='12345678901',
					email='nicolaihygino2000@gmail.com', phone='21-98258-5168')
		self.resp = self.client.post(r('subscriptions:new'), self.data)

	def test_post(self):
		"""valid POST should redirect to /inscricao/1/"""
		hash_name = hashlib.md5(self.data['name'].encode()).hexdigest()
		hash_cpf = hashlib.md5(self.data['cpf'].encode()).hexdigest()
		hash_url = ''.join([hash_name, hash_cpf])
		self.assertRedirects(self.resp, r('subscriptions:detail', hash_url))
	
	def test_send_subscribe_email(self):
		self.assertEqual(1, len(mail.outbox))

	def test_save_subscription(self):
		self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
	def setUp(self):
		self.resp = self.client.post(r('subscriptions:new'), {})

	def test_post(self):
		"""Invalid POST shoult not redirect"""
		self.assertEqual(200, self.resp.status_code)

	def test_template(self):
		self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

	def test_has_form(self):
		form = self.resp.context['form']
		self.assertIsInstance(form, SubscriptionForm)

	def test_form_has_errors(self):
		form = self.resp.context['form']
		self.assertTrue(form.errors)

	def test_dont_save_subscription(self):
		self.assertFalse(Subscription.objects.exists())


class TemplateRegressionTest(TestCase):
	def test_template_has_non_field_errors(self):
		invalid_data = dict(name='Nicolai Hygino', cpf='12345678901')
		response = self.client.post(r('subscriptions:new'), invalid_data)

		self.assertContains(response, '<ul class="errorlist nonfield">')