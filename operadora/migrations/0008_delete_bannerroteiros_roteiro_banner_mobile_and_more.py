# Generated by Django 5.2.2 on 2025-06-07 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operadora', '0007_bannerroteiros'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BannerRoteiros',
        ),
        migrations.AddField(
            model_name='roteiro',
            name='banner_mobile',
            field=models.ImageField(blank=True, help_text='480x720 para celular', null=True, upload_to='roteiros/banners/'),
        ),
        migrations.AddField(
            model_name='roteiro',
            name='banner_pc',
            field=models.ImageField(blank=True, help_text='1920x500 para desktop e tablet', null=True, upload_to='roteiros/banners/'),
        ),
    ]
