from django.db import models
import imovel.models

# Create your models here.
class Transacao(models.Model):
    codigoTransacao = models.CharField('Código da Transação', max_length=10, unique=True, default='Transação')
    codigoImovel = models.ForeignKey('imovel.Imovel', on_delete=models.CASCADE, verbose_name='Código do Imóvel')
    codigoCorretor = models.ForeignKey('corretores.Corretor', on_delete=models.CASCADE, verbose_name='Código do Corretor')
    codigoCliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, verbose_name='Código do Cliente')
    tipoTransacao = models.CharField('Tipo de Transação', max_length=20, choices=[('Venda', 'Venda'), ('Aluguel', 'Aluguel')])
    dataTransacao = models.DateField('Data da Transação')
    statusTransacao = models.CharField('Status da Transação', max_length=20, choices=[('Pendente', 'Pendente'), ('Concluída', 'Concluída'), ('Cancelada', 'Cancelada')])
    valorVenda = models.DecimalField('Valor da Venda', max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    def __str__(self):
        return f"Transação {self.codigoTransacao}"