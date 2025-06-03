from django.db import models
from stdimage.models import StdImageField
from proprietarios.models import Proprietario
from transacao.models import Transacao

class Imovel(models.Model):  
    nome = models.CharField(max_length=100)  
    codigoImovel = models.CharField('Código do Imóvel', max_length=10, unique=True, help_text='Código único do imóvel', default='Imovel')
    foto = StdImageField('Foto', upload_to='pessoas', delete_orphans=True, null=True, blank=True)  
    endereco = models.CharField('Endereço', max_length=100, help_text='Endereço completo')
    proprietario = models.ManyToManyField(Proprietario, verbose_name='Proprietário', help_text='Selecione o proprietário do imóvel')
    disponivel_locacao = models.BooleanField('Disponível para Locação', default=True, help_text='Indica se o imóvel está disponível para locação')

    valorVenda = models.DecimalField('Valor de Venda', max_digits=10, decimal_places=2, null=True, blank=True, help_text='Valor do imóvel para venda')
    valorIPTU = models.DecimalField('Valor IPTU', max_digits=10, decimal_places=2, null=True, blank=True, help_text='Valor anual do IPTU')
    valorCondominio = models.DecimalField('Valor do Condomínio', max_digits=10, decimal_places=2, null=True, blank=True, help_text='Valor mensal do condomínio')
    
    areaTotal = models.DecimalField('Área Total (m²)', max_digits=10, decimal_places=2, null=True, blank=True, help_text='Área total do imóvel em metros quadrados')
    areaPrivativa = models.DecimalField('Área Privativa (m²)', max_digits=10, decimal_places=2, null=True, blank=True, help_text='Área privativa do imóvel em metros quadrados')
    areaUtil = models.DecimalField('Área Útil (m²)', max_digits=10, decimal_places=2, null=True, blank=True, help_text='Área útil do imóvel em metros quadrados')
    
    numQuartos = models.IntegerField('Número de Quartos', null=True, blank=True, help_text='Número de quartos no imóvel')
    numBanheiros = models.IntegerField('Número de Banheiros', null=True, blank=True, help_text='Número de banheiros no imóvel')
    vagasGaragem = models.IntegerField('Vagas de Garagem', null=True, blank=True, help_text='Número de vagas de garagem disponíveis')

    caracteristicas = models.TextField('Características', null=True, blank=True, help_text='Descrição das características do imóvel')
    comodidades = models.TextField('Comodidades', null=True, blank=True, help_text='Lista de comodidades oferecidas pelo imóvel')
    descricao = models.TextField('Descrição Completa', null=True, blank=True, help_text='Descrição detalhada do imóvel')

    tipoImovel = models.CharField('Tipo de Imóvel', max_length=20, choices=[('Casa', 'Casa'), ('Apartamento', 'Apartamento'), ('Terreno', 'Terreno'), ('Comercial', 'Comercial'), ('Outro', 'Outro'),], null=True, blank=True, help_text='Tipo do imóvel (casa, apartamento, etc.)')

    class Meta:  
        verbose_name = 'Imóvel'  
        verbose_name_plural = 'Imóveis'  

    def __str__(self):  
        return self.nome
    
    def has_proprietarios(self):
        return self.proprietario.exists()
    
    def status_imovel(self):
        if Transacao.objects.filter(codigoImovel=self, tipoTransacao='Venda', statusTransacao='Pendente').exists():
            return 'Em Confirmação de Venda'
        elif not self.disponivel_locacao:
            return 'Não Disponível para Locação'
        else:
            return 'Disponível para Locação e Venda'