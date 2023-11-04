from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    avatar = models.ImageField(upload_to="avatar", null=True)
    telefone = models.ImageField(max_length=200, null=False, blank=False)
    telefone = models.CharField(max_length=200, null=False, blank=False)
    cpf_cnpj = models.CharField(max_length=200, null=False, blank=False)
    data_nascimento = models.DateField(null=False)
    is_active = models.BooleanField(null=False)
    user_cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "loja_cliente"

    def __str__(self):
        return str(self.id)


class Endereco(models.Model):
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    cep = models.CharField(max_length=200, null=False, blank=False)
    estado = models.CharField(max_length=200, null=False, blank=False)
    cidade = models.CharField(max_length=200, null=False, blank=False)
    bairro = models.CharField(max_length=200, null=True, blank=False)
    logradouro = models.CharField(max_length=200, null=True, blank=False)
    nr_casa = models.IntegerField(null=True, blank=False)
    user_cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "loja_cliente_endereco"

    def __str__(self):
        return self.id
