# Generated by Django 5.2 on 2025-07-07 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imovel', '0010_imovel_valoraluguel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='valorAluguel',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor do Aluguel'),
        ),
    ]
