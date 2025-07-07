from django.db import models
from stdimage.models import StdImageField
from proprietarios.models import Proprietario
from transacao.models import Transacao
from decimal import Decimal
from django.utils import timezone
from django.core.exceptions import ValidationError

class Imovel(models.Model):  
    nome = models.CharField(max_length=100)  
    codigoImovel = models.CharField('Código do Imóvel', max_length=10, unique=True, help_text='Código único do imóvel') 
    foto = StdImageField('Foto', upload_to='pessoas', delete_orphans=True, null=True, blank=True)  
    rua = models.CharField('Rua', max_length=100, help_text='Nome da rua do imóvel', null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=100, help_text='Bairro onde o imóvel está localizado', null=True, blank=True)
    cidade = models.CharField('Cidade', max_length=100, help_text='Cidade onde o imóvel está localizado', null=True, blank=True)
    estado = models.CharField('Estado', max_length=100, help_text='Estado onde o imóvel está localizado', null=True, blank=True)
    cep = models.CharField('CEP', max_length=10, help_text='Código Postal do imóvel', null=True, blank=True)
    numero = models.CharField('Número', max_length=10, help_text='Número do imóvel no endereço', null=True, blank=True)
    complemento = models.CharField('Complemento', max_length=50, null=True, blank=True, help_text='Complemento do endereço (ex: apartamento, bloco)')
    proprietario = models.ManyToManyField(Proprietario, verbose_name='Proprietário',)
    disponivel_locacao = models.BooleanField('Disponível para Locação', default=True, )
    valorVenda = models.DecimalField('Valor de Venda', max_digits=10, decimal_places=2, null=True, blank=True )
    valorIPTU = models.DecimalField('Valor IPTU', max_digits=10, decimal_places=2, null=True, blank=True)
    valorCondominio = models.DecimalField('Valor do Condomínio', max_digits=10, decimal_places=2, null=True, blank=True )
    areaTotal = models.DecimalField('Área Total (m²)', max_digits=10, decimal_places=2, null=True, blank=True)
    areaPrivativa = models.DecimalField('Área Privativa (m²)', max_digits=10, decimal_places=2, null=True, blank=True)
    areaUtil = models.DecimalField('Área Útil (m²)', max_digits=10, decimal_places=2, null=True, blank=True)
    numQuartos = models.IntegerField('Número de Quartos', null=True, blank=True,)
    numBanheiros = models.IntegerField('Número de Banheiros', null=True, blank=True,)
    vagasGaragem = models.IntegerField('Vagas de Garagem', null=True, blank=True,)
    caracteristicas = models.TextField('Características', null=True, blank=True, )
    comodidades = models.TextField('Comodidades', null=True, blank=True,)
    descricao = models.TextField('Descrição Completa', null=True, blank=True, )
    tipoImovel = models.CharField('Tipo de Imóvel', max_length=20, choices=[('Casa', 'Casa'), ('Apartamento', 'Apartamento'), ('Terreno', 'Terreno'), ('Comercial', 'Comercial'), ('Outro', 'Outro'),], null=True, blank=True)
    last_updated = models.DateTimeField('Última Atualização', auto_now=True, help_text='Data e hora da última atualização do imóvel')

    valorAluguel = models.DecimalField('Valor do Aluguel', max_digits=10, decimal_places=2, null=True, blank=True)



    VALORIZACAO_PADRAO = Decimal('1.10')  

    zona_valorizacao = models.BooleanField(
        'Zona de Valorização',
        default=False, 
        help_text="Marque se o imóvel está em uma região de valorização especial (ex: bairro de luxo, próximo a universidades)."
    )

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
            
    def calcular_valor_venda_com_valorizacao(self):
        if self.valorVenda is None:
            return None
        
        if self.zona_valorizacao:
            return self.valorVenda * self.VALORIZACAO_PADRAO
        return self.valorVenda
    
    def is_outdated(self):
        six_months_ago = timezone.now() - timezone.timedelta(days=180) 
        return self.last_updated < six_months_ago
    
    def pendencia_transacao(self):
        return Transacao.objects.filter(codigoImovel=self, statusTransacao='Pendente').exists()
    
    def get_valor_venda_br(self):
        if self.valorVenda is None:
            return None
        return f"{self.valorVenda:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


    def save(self, *args, **kwargs):
        if not self.codigoImovel:  
            iniciais = self.__class__.__name__[:2].upper()  
            finais = self.__class__.__name__[-2:].upper()   
            ultimo_imovel = Imovel.objects.order_by('-codigoImovel').first()
            if ultimo_imovel:  
                numero = int(ultimo_imovel.codigoImovel[2:-2]) + 1
            else:  
                numero = 1
            self.codigoImovel = f"{iniciais}{numero:03d}{finais}"
        super().save(*args, **kwargs)  

    def delete(self, *args, **kwargs):
        if self.imovel_visitas.exists(): 
            raise ValidationError("Não é possível excluir o imóvel pois existem visitas agendadas ou realizadas associadas a ele.")
        if self.transacao_set.exists():
            raise ValidationError("Não é possível excluir o imóvel pois existem transações associadas a ele.")
        super().delete(*args, **kwargs)