from django.test import TestCase
from unittest.mock import Mock
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin

class SubscriptionModelAdminTest(TestCase):
	def setUp(self):
		Subscription.objects.create(name='Nicolai Hygino', cpf='01234567890',
									email='nicolaihygino2000@gmail.com', phone='21 98258-5168', 
									paid='True')
		self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)

	def test_has_action(self):
		"""Action desmark_paid should be instaled"""
		self.assertIn('desmark_paid', self.model_admin.actions)

	def test_desmark_all(self):
		"""It shout desmark all selectec option as paid"""
		self.call_action()
		self.assertEqual(1, Subscription.objects.filter(paid=False).count())

	def test_message(self):
		mock = self.call_action()
		mock.assert_called_once_with(None, '1 inscrição foi desmarcada como paga.')

	def call_action(self):
		queryset = Subscription.objects.all()
		
		mock = Mock()
		old_messege_user = SubscriptionModelAdmin.message_user
		SubscriptionModelAdmin.message_user = mock

		self.model_admin.desmark_paid(None, queryset)

		SubscriptionModelAdmin.message_user = old_messege_user

		return mock
