# Generated by Django 5.2.2 on 2025-06-05 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operadora', '0002_boxproduto_slide_unidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
