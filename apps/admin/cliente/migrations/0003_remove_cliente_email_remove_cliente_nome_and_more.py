# Generated by Django 4.1.2 on 2022-11-08 00:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cliente", "0002_remove_cliente_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cliente",
            name="email",
        ),
        migrations.RemoveField(
            model_name="cliente",
            name="nome",
        ),
        migrations.RemoveField(
            model_name="cliente",
            name="senha",
        ),
        migrations.RemoveField(
            model_name="endereco",
            name="cliente",
        ),
        migrations.AddField(
            model_name="cliente",
            name="user_cliente",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="endereco",
            name="user_cliente",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
