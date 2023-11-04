from django.db import models


class Auditoria(models.Model):
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    user = models.CharField(max_length=200, null=False, blank=False)
    mensagem = models.CharField(max_length=200, null=False, blank=False)
    ip = models.CharField(max_length=200, null=False, blank=False)
    data = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        db_table = "administrador_auditoria"

    def __str__(self):
        return self.id
