from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
	def test_form_has_fields(self):
		"""Form must have 4 fields"""
		form = SubscriptionForm()
		expected = ['name', 'cpf', 'email', 'phone']
		self.assertSequenceEqual(expected, list(form.fields))

	def test_cpf_is_digit(self):
		"""CPF must only accepts digits."""	
		form = self.make_validated_form(cpf='ACBD5678901')
		self.assertFormErrorCode(form, 'cpf', 'digits')

	def test_cpf_has_11_digits(self):
		"""CPF must have 11 digits"""
		form = self.make_validated_form(cpf='1234')
		self.assertFormErrorCode(form, 'cpf', 'length')

	def test_email_is_optional(self):
		"""Email is optional"""
		form = self.make_validated_form(email='')
		self.assertFalse(form.errors)

	def test_phone_is_optional(self):
		"""Phone is optional"""
		form = self.make_validated_form(phone='')
		self.assertFalse(form.errors)

	def test_must_inform_email_or_phone(self):
		"""Email and phone are optional, but one must be informed."""
		form = self.make_validated_form(email='', phone='')
		self.assertListEqual(['__all__'], list(form.errors))

	def test_name_must_be_capitalized(self):
		"""Name Must Be Capitalized"""
		form = self.make_validated_form(name='NICOLAI hygino')
		self.assertEqual('Nicolai Hygino', form.cleaned_data['name'])

	def test_phone_is_digit(self):
		"""Phone must only accepts digits"""
		form = self.make_validated_form(phone='ABCD56789')
		#self.assertListEqual(['phone'], list(form.errors))
		self.assertFormErrorCode(form, 'phone', 'phone-digits')

	def assertFormErrorCode(self, form, field, code):
		errors = form.errors.as_data()
		errors_list = errors[field]
		exception = errors_list[0]
		self.assertEqual(code, exception.code)

	def assertFormErrorMessage(self, form, field, msg):
		errors = form.errors
		errors_list = errors[field]
		self.assertListEqual([msg], errors_list)

	def make_validated_form(self, **kwargs):
		valid = dict(name='Nicolai Hygino', cpf='12345678901',
					email='nicolaihygino2000@gmail.com', phone='21 98258-5168')
		data = dict(valid, **kwargs)
		form = SubscriptionForm(data)
		form.is_valid()
		
		return form
