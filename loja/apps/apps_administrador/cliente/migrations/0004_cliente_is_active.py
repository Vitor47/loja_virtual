# Generated by Django 4.1.2 on 2022-11-15 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_remove_cliente_email_remove_cliente_nome_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
