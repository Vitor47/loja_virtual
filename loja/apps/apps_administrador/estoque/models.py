from django.db import models

class Configuracao(models.Model):
    id = models.IntegerField(null=False, primary_key=True, auto_created=True),
    nome = models.CharField(max_length=200, null=False, blank=False)
    quantidade = models.IntegerField(null=False, blank=False)
    valor_estoque = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = "administrador_estoque"

    def __str__(self):
        return self.id
