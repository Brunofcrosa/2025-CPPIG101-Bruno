# Generated by Django 5.2 on 2025-05-23 01:48

import stdimage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proprietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=15)),
                ('foto', stdimage.models.StdImageField(blank=True, force_min_size=False, null=True, upload_to='pessoas', variations={}, verbose_name='Foto')),
                ('endereco', models.CharField(blank=True, max_length=255, null=True)),
                ('codigoProprietario', models.IntegerField(help_text='Código do proprietário', max_length=10, unique=True, verbose_name='Código do Proprietário')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
