from django.db import models
import uuid


class Subscription(models.Model):
	hash_url = models.CharField('URL', max_length=32, null=True)
	name = models.CharField('nome', max_length=100)
	cpf = models.CharField('CPF', max_length=11)
	email = models.EmailField('email')
	phone = models.CharField('telefone', max_length=20)
	created_at = models.DateTimeField('criado em', auto_now_add=True)
	paid = models.BooleanField('pago', default=False)

	class Meta:
		verbose_name_plural = 'inscrições'
		verbose_name = 'inscrição'
		ordering = ('-created_at',)

	def __str__(self):
		return self.name