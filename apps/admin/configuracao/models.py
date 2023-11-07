from django.db import models


class Configuracao(models.Model):  
    nome = models.CharField(max_length=200, null=False, blank=False)
    valor = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = "administrador_configuracao"

    def __str__(self):
        return self.id
