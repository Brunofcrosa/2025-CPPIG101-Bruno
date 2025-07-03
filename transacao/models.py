import re
from django.db import models
import imovel.models
from decimal import Decimal 
# Create your models here.
class Transacao(models.Model):
    codigoTransacao = models.CharField('Código da Transação', max_length=10, unique=True) 
    codigoImovel = models.ForeignKey('imovel.Imovel', on_delete=models.CASCADE, verbose_name='Código do Imóvel')
    codigoCorretor = models.ForeignKey('corretores.Corretor', on_delete=models.CASCADE, verbose_name='Código do Corretor')
    codigoCliente = models.ForeignKey('cliente.Cliente', on_delete=models.CASCADE, verbose_name='Código do Cliente')
    tipoTransacao = models.CharField('Tipo de Transação', max_length=20, choices=[('Venda', 'Venda'), ('Aluguel', 'Aluguel')])
    dataTransacao = models.DateField('Data da Transação')
    statusTransacao = models.CharField('Status da Transação', max_length=20, choices=[('Pendente', 'Pendente'), ('Concluída', 'Concluída'), ('Cancelada', 'Cancelada')])
    valorVenda = models.DecimalField('Valor da Venda', max_digits=10, decimal_places=2, null=True, blank=True)
    valorComissao = models.DecimalField('Valor da Comissão', max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    def __str__(self):
        return f"Transação {self.codigoTransacao}"
    
    def save(self, *args, **kwargs):
        if not self.codigoTransacao:
            nome_modelo = self.__class__.__name__
            prefixo = nome_modelo[0:2].upper()
            sufixo = nome_modelo[-2:].upper()

            padrao = re.compile(rf"^{prefixo}(\d+){sufixo}$")
            
            ultimo_numero_sequencial = 99
            
            todos_os_codigos_do_modelo = self.__class__.objects.filter(
                codigoTransacao__startswith=prefixo,
                codigoTransacao__endswith=sufixo
            ).values_list('codigoTransacao', flat=True)

            for codigo in todos_os_codigos_do_modelo:
                correspondencia = padrao.match(codigo)
                if correspondencia:
                    try:
                        numero_atual = int(correspondencia.group(1))
                        if numero_atual > ultimo_numero_sequencial:
                            ultimo_numero_sequencial = numero_atual
                    except ValueError:
                        pass
            
            proximo_numero_sequencial = ultimo_numero_sequencial + 1
            self.codigoTransacao = f"{prefixo}{proximo_numero_sequencial:03d}{sufixo}"


        TAXA_VENDA_NORMAL = Decimal('0.05')  
        TAXA_ALUGUEL_NORMAL = Decimal('0.08') 
        TAXA_VENDA_VALORIZACAO = Decimal('0.07') 
        TAXA_ALUGUEL_VALORIZACAO = Decimal('0.10')

        if self.valorVenda is not None:
            if self.tipoTransacao == 'Venda':
                if self.codigoImovel.zona_valorizacao:
                    self.valorComissao = self.valorVenda * TAXA_VENDA_VALORIZACAO
                else:
                    self.valorComissao = self.valorVenda * TAXA_VENDA_NORMAL
            elif self.tipoTransacao == 'Aluguel':
                if self.codigoImovel.zona_valorizacao:
                    self.valorComissao = self.valorVenda * TAXA_ALUGUEL_VALORIZACAO
                else:
                    self.valorComissao = self.valorVenda * TAXA_ALUGUEL_NORMAL
        
        super().save(*args, **kwargs)