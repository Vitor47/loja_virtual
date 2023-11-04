from django.contrib.auth.models import User
from django.db import models


class Banner(models.Model):
    id = (models.IntegerField(null=False, primary_key=True, auto_created=True),)
    status = models.BooleanField(null=False)
    imagem = models.ImageField(upload_to="banner")
    data_cad = models.DateField(null=False)
    dat_edit = models.DateField(null=True)
    user_cad = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    class Meta:
        db_table = "administrador_banner"

    def __str__(self):
        return self.id
