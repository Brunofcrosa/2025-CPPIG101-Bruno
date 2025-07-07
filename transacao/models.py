from django.db import models
from decimal import Decimal

class Transacao(models.Model):
    codigoTransacao = models.CharField('Código da Transação', max_length=10, unique=True)
    codigoImovel = models.ForeignKey('imovel.Imovel', on_delete=models.CASCADE, verbose_name='Imóvel:')
    codigoCorretor = models.ForeignKey('corretores.Corretor', on_delete=models.CASCADE, verbose_name='Corretor:')
    codigoCliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, verbose_name='Cliente:')
    tipoTransacao = models.CharField('Tipo:', max_length=20, choices=[('Venda', 'Venda'), ('Aluguel', 'Aluguel')])
    dataTransacao = models.DateField('Data:')
    statusTransacao = models.CharField('Status:', max_length=20, choices=[('Pendente', 'Pendente'), ('Concluída', 'Concluída'), ('Cancelada', 'Cancelada')])
    valorVenda = models.DecimalField('Valor da Venda:', max_digits=10, decimal_places=2, null=True, blank=True)
    valorComissao = models.DecimalField('Valor da Comissão:', max_digits=10, decimal_places=2, null=True, blank=True)

    valorAluguelMensal = models.DecimalField('Valor do Aluguel Mensal:', max_digits=10, decimal_places=2, null=True, blank=True)
    dataInicioAluguel = models.DateField('Data de Início do Aluguel:', null=True, blank=True)
    dataFimAluguel = models.DateField('Data de Fim do Aluguel:', null=True, blank=True)
    diaVencimentoAluguel = models.IntegerField('Dia de Vencimento do Aluguel:', null=True, blank=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    def __str__(self):
        return f"Transação {self.codigoTransacao}"

    def save(self, *args, **kwargs):
        if not self.codigoTransacao:
            iniciais = self.__class__.__name__[:2].upper()
            finais = self.__class__.__name__[-2:].upper()
            ultima_transacao = Transacao.objects.order_by('-codigoTransacao').first()
            if ultima_transacao:
                numero = int(ultima_transacao.codigoTransacao[2:-2]) + 1
            else:
                numero = 1
            self.codigoTransacao = f"{iniciais}{numero:03d}{finais}"

        TAXA_VENDA_NORMAL = Decimal('0.05')
        TAXA_ALUGUEL_NORMAL = Decimal('0.08')
        TAXA_VENDA_VALORIZACAO = Decimal('0.07')
        TAXA_ALUGUEL_VALORIZACAO = Decimal('0.10')

        if self.tipoTransacao == 'Venda' and self.valorVenda is not None:
            if self.codigoImovel.zona_valorizacao:
                self.valorComissao = self.valorVenda * TAXA_VENDA_VALORIZACAO
            else:
                self.valorComissao = self.valorVenda * TAXA_VENDA_NORMAL
        elif self.tipoTransacao == 'Aluguel' and self.valorAluguelMensal is not None:
            if self.codigoImovel.zona_valorizacao:
                self.valorComissao = self.valorAluguelMensal * TAXA_ALUGUEL_VALORIZACAO
            else:
                self.valorComissao = self.valorAluguelMensal * TAXA_ALUGUEL_NORMAL
        else:
            self.valorComissao = None 

        super().save(*args, **kwargs)