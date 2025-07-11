# Generated by Django 5.2 on 2025-07-07 19:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0007_alter_cliente_email_alter_cliente_endereco_and_more'),
        ('corretores', '0006_alter_corretor_email_alter_corretor_endereco_and_more'),
        ('imovel', '0009_alter_imovel_areaprivativa_alter_imovel_areatotal_and_more'),
        ('transacao', '0004_alter_transacao_codigotransacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao',
            name='dataFimAluguel',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Fim do Aluguel:'),
        ),
        migrations.AddField(
            model_name='transacao',
            name='dataInicioAluguel',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Início do Aluguel:'),
        ),
        migrations.AddField(
            model_name='transacao',
            name='diaVencimentoAluguel',
            field=models.IntegerField(blank=True, null=True, verbose_name='Dia de Vencimento do Aluguel:'),
        ),
        migrations.AddField(
            model_name='transacao',
            name='valorAluguelMensal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor do Aluguel Mensal:'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='codigoCliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.cliente', verbose_name='Cliente:'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='codigoCorretor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corretores.corretor', verbose_name='Corretor:'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='codigoImovel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imovel.imovel', verbose_name='Imóvel:'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='dataTransacao',
            field=models.DateField(verbose_name='Data:'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='statusTransacao',
            field=models.CharField(choices=[('Pendente', 'Pendente'), ('Concluída', 'Concluída'), ('Cancelada', 'Cancelada')], max_length=20, verbose_name='Status:'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='tipoTransacao',
            field=models.CharField(choices=[('Venda', 'Venda'), ('Aluguel', 'Aluguel')], max_length=20, verbose_name='Tipo:'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='valorComissao',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor da Comissão:'),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='valorVenda',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Valor da Venda:'),
        ),
    ]
