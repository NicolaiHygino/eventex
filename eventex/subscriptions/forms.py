from django import forms
import string
from django.core.exceptions import ValidationError


def validate_cpf(value):
	if not value.isdigit():
		raise ValidationError('CPF deve conter apenas números.', 'digits')

	if len(value) != 11:
		raise ValidationError('CPF deve ter 11 números.', 'length')

def validate_phone(value):
	for x in string.ascii_letters:
		if x in value:
			raise ValidationError('Telefone deve apenas conter números.', 'phone-digits')

class SubscriptionForm(forms.Form):
	name = forms.CharField(label='Nome')
	cpf = forms.CharField(label='CPF', validators=[validate_cpf])
	email = forms.EmailField(label='Email', required=False)
	phone = forms.CharField(label='Telefone', required=False, validators=[validate_phone])

	def clean_name(self):
		name = self.cleaned_data['name']
		words = [w.capitalize() for w in name.split()]
		return ' '.join(words)

	def clean(self):
		if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
			raise ValidationError('Informe seu e-mail ou telefone.')