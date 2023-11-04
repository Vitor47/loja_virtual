"""from django.db import models
from django.contrib.auth.models import User
from ..apps_administrador.produto.models import Produto

class StatusCarrinho(models.Model):
	id = models.IntegerField(null=False, primary_key=True, auto_created=True),
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=False)
	data_cad = models.DateTimeField(null=False, auto_created=True)

	class Meta:
		db_table = "loja_status_carrinho"

	def __str__(self):
		return self.id"""
