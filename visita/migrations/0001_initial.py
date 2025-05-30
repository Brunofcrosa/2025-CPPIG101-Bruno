# Generated by Django 5.2 on 2025-05-26 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0004_cliente_codigocliente_alter_cliente_endereco'),
        ('corretores', '0001_initial'),
        ('imovel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(help_text='Data da visita', null=True, verbose_name='Data')),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cliente', to='cliente.cliente')),
                ('corretor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corretor', to='corretores.corretor')),
                ('imovel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imovel', to='imovel.imovel')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
    ]
