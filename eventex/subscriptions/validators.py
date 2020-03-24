from django.core.exceptions import ValidationError

import string


def validate_cpf(value):
	if not value.isdigit():
		raise ValidationError('CPF deve conter apenas números.', 'digits')

	if len(value) != 11:
		raise ValidationError('CPF deve ter 11 números.', 'length')

def validate_phone(value):
	for x in string.ascii_letters:
		if x in value:
			raise ValidationError('Telefone deve apenas conter números.', 'phone-digits')