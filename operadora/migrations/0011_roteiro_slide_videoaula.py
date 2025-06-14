# Generated by Django 5.2.2 on 2025-06-07 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operadora', '0010_delete_bannerroteiros_delete_roteiro_delete_slide_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roteiro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True)),
                ('arquivo', models.FileField(upload_to='roteiros/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='roteiros/thumbnails/')),
                ('icone', models.CharField(blank=True, choices=[('fas fa-book', 'Livro'), ('fas fa-map', 'Mapa'), ('fas fa-globe', 'Globo'), ('fas fa-plane', 'Avião'), ('fas fa-mountain', 'Montanha'), ('fas fa-file-pdf', 'PDF'), ('fas fa-umbrella-beach', 'Praia')], max_length=50)),
                ('banner_pc', models.ImageField(blank=True, help_text='1920x500 para desktop e tablet', null=True, upload_to='roteiros/banners/')),
                ('banner_mobile', models.ImageField(blank=True, help_text='480x720 para celular', null=True, upload_to='roteiros/banners/')),
                ('data_publicacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Roteiros',
            },
        ),
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField(max_length=300)),
                ('imagem', models.ImageField(upload_to='slides/')),
                ('link', models.URLField(blank=True, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('ordem', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Home',
            },
        ),
        migrations.CreateModel(
            name='VideoAula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('categoria', models.CharField(choices=[('terra_santa', 'Terra Santa'), ('treinamento', 'Treinamento Empresarial'), ('dubai', 'Dubai'), ('eua', 'Estados Unidos')], max_length=20)),
                ('descricao', models.TextField()),
                ('url', models.URLField()),
                ('thumbnail', models.ImageField(upload_to='videos/thumbnails/')),
                ('data_publicacao', models.DateTimeField(auto_now_add=True)),
                ('ordem', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Aulas',
            },
        ),
    ]
