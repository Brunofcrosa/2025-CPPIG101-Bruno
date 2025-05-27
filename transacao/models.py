from django.db import models
import imovel.models

# Create your models here.
class Transacao(models.Model):
    codigoTransacao = models.CharField('Código do Transacao', max_length=10, unique=True, help_text='Código único do Transacao', default='Transacao')
    codigoImovel = models.ForeignKey('imovel.Imovel', on_delete=models.CASCADE, verbose_name='Código do Imóvel', help_text='Código do Imóvel relacionado à transação')
    codigoCorretor = models.ForeignKey('corretores.Corretor', on_delete=models.CASCADE, verbose_name='Código do Corretor', help_text='Código do Corretor relacionado à transação')
    codigoCliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, verbose_name='Código do Cliente', help_text='Código do Cliente relacionado à transação')
    tipoTransacao = models.CharField('Tipo de Transação', max_length=20, choices=[('Venda', 'Venda'), ('Aluguel', 'Aluguel')], help_text='Tipo de transação (Venda ou Aluguel)')
    dataTransacao = models.DateField('Data da Transação', help_text='Data em que a transação foi realizada')
    statusTransacao = models.CharField('Status da Transação', max_length=20, choices=[('Pendente', 'Pendente'), ('Concluída', 'Concluída'), ('Cancelada', 'Cancelada')], help_text='Status atual da transação')
    valorVenda = models.DecimalField('Valor da Venda', max_digits=10, decimal_places=2, null=True, blank=True, help_text='Valor da venda do imóvel (se aplicável)')

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    def __str__(self):
        return f"Transação {self.codigoTransacao}"