# Generated by Django 5.2 on 2025-04-26 22:30

import stdimage.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_alter_cliente_options_alter_cliente_endereco'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='foto',
            field=stdimage.models.StdImageField(blank=True, force_min_size=False, null=True, upload_to='pessoas', variations={}, verbose_name='Foto'),
        ),
    ]
