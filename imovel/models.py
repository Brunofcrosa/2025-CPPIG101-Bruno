from django.db import models

class Imovel(models.Model):
    codigoImovel = models.IntegerField('codigoImovel', help_text='Código do Imóvel', unique=True)
    endereco = models.CharField('endereco', max_length=70, help_text='Endereço do Imóvel')
    proprietario = models.CharField('proprietario', max_length=70, help_text='Proprietário do Imóvel')
    tipoTransacao = models.CharField('tipoTransacao', max_length=70, help_text='Tipo da Transação')
    valorVenda = models.DecimalField('valorVenda', max_digits=10, decimal_places=2, help_text='Valor de Venda')
    valorIPTU = models.DecimalField('valorIPTU', max_digits=10, decimal_places=2, help_text='Valor do IPTU')
    valorCondominio = models.DecimalField('valorCondominio', max_digits=10, decimal_places=2, help_text='Valor do Condomínio')
    areaTotal = models.DecimalField('areaTotal', max_digits=10, decimal_places=2, help_text='Área total do Imóvel')
    areaPrivativa = models.DecimalField('areaPrivativa', max_digits=10, decimal_places=2, help_text='Área Privativa do Imóvel')
    areaUtil = models.DecimalField('areaUtil', max_digits=10, decimal_places=2, help_text='Área Útil do Imóvel')
    numQuartos = models.IntegerField('numQuartos', help_text='Número de Quartos do Imóvel')
    numBanheiros = models.IntegerField('numBanheiros', help_text='Número de Banheiros do Imóvel')
    vagasGaragem = models.IntegerField('vagasGaragem', help_text='Vagas de Garagem')
    tipoImovel = models.CharField('tipoImovel', max_length=70, help_text='Tipo de Imóvel')
    caracteristicasImovel = models.CharField('caracteristicasImovel', max_length=70, help_text='Características do Imóvel')
    comodidades = models.CharField('comodidadesImovel', max_length=70, help_text='Comodidades do Imóvel')
    descricaoImovel = models.CharField('descricaoImovel', max_length=70, help_text='Descrição do Imóvel')

    def __str__(self):
        return f"Imóvel {self.codigoImovel} - {self.endereco}"
