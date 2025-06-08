from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from localflavor.br.br_states import STATE_CHOICES
import requests


class Operadora(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    FONTE_CONHECIMENTO_CHOICES = [
        ('site', 'Site'),
        ('google', 'Google'),
        ('indicacao', 'Indicação'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cnpj = models.CharField(max_length=18, unique=True)
    razao_social = models.CharField(max_length=100)
    nome_fantasia = models.CharField(max_length=100)
    data_abertura = models.DateField()
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2, choices=STATE_CHOICES)
    site = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    fonte_conhecimento = models.CharField(max_length=20, choices=FONTE_CONHECIMENTO_CHOICES)
    logomarca = models.ImageField(upload_to='operadoras/logomarcas/', blank=True)
    
    # Dados do representante legal
    nome_representante = models.CharField(max_length=100)
    email_representante = models.EmailField()
    telefone_comercial1 = models.CharField(max_length=15)
    telefone_comercial2 = models.CharField(max_length=15, blank=True)
    celular_representante = models.CharField(max_length=15)
    data_nascimento_representante = models.DateField()    
    ativo = models.BooleanField(default=False)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome_fantasia
    
    def clean(self):
        """Validação personalizada para o CEP"""
        if self.cep and not all([self.logradouro, self.bairro, self.cidade, self.uf]):
            try:
                response = requests.get(f'https://viacep.com.br/ws/{self.cep}/json/')
                if response.status_code == 200:
                    data = response.json()
                    if not data.get('erro'):
                        self.logradouro = data.get('logradouro', '')
                        self.bairro = data.get('bairro', '')
                        self.cidade = data.get('localidade', '')
                        self.uf = data.get('uf', '')
            except requests.RequestException:
                raise ValidationError('Erro ao consultar o CEP')
    
    def save(self, *args, **kwargs):
        self.clean()  # Executa a validação antes de salvar
        super().save(*args, **kwargs)

class VideoAula(models.Model):
    CATEGORIA_CHOICES = [
        ('terra_santa', 'Terra Santa'),
        ('treinamento', 'Treinamento Empresarial'),
        ('dubai', 'Dubai'),
        ('eua', 'Estados Unidos'),
    ]
    
    titulo = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    descricao = models.TextField()
    url = models.URLField()  # YouTube ou .mp4
    thumbnail = models.ImageField(upload_to='videos/thumbnails/')
    data_publicacao = models.DateTimeField(auto_now_add=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']
    
    class Meta:
        verbose_name = 'Aula'
    
    def __str__(self):
        return self.titulo

class Roteiro(models.Model):
    ICONES_CHOICES = [
        ('fas fa-book', 'Livro'),
        ('fas fa-map', 'Mapa'),
        ('fas fa-globe', 'Globo'),
        ('fas fa-plane', 'Avião'),
        ('fas fa-mountain', 'Montanha'),
        ('fas fa-file-pdf', 'PDF'),
        ('fas fa-umbrella-beach', 'Praia'),
    ]

    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    arquivo = models.FileField(upload_to='roteiros/')
    thumbnail = models.ImageField(upload_to='roteiros/thumbnails/', blank=True, null=True)
    icone = models.CharField(max_length=50, choices=ICONES_CHOICES, blank=True)
    banner_pc = models.ImageField(upload_to='roteiros/banners/', blank=True, null=True, help_text="1920x500 para desktop e tablet")
    banner_mobile = models.ImageField(upload_to='roteiros/banners/', blank=True, null=True, help_text="480x720 para celular")
    data_publicacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Incluir Roteiro'
        verbose_name = 'Roteiro'

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='fornecedores/logos/')
    website = models.URLField(blank=True)
    pais = models.CharField(max_length=100, verbose_name="País de origem", blank=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='produtos/')
    arquivo = models.FileField(upload_to='produtos/downloads/', blank=True)
    link = models.URLField(blank=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nome
    
#MODELS DA HOME

class Slide(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=300)
    imagem = models.ImageField(upload_to='slides/')
    link = models.URLField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides'
    

class BoxProduto(models.Model):
    TIPO_CHOICES = [
        ('Corporativo', 'Corporativo'),
        ('Religioso', 'Religioso'),
        ('Intercâmbio', 'Intercâmbio'),
        ('Lazer', 'Lazer'),
    ]
    ativo = models.BooleanField(default=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    imagem = models.ImageField(upload_to='box_produtos/')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(max_length=250)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class Unidade(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='unidades/')
    logo = models.ImageField(upload_to='logos/')
    link = models.URLField()

    def __str__(self):
        return self.nome

#EMAILS DA EQUIPE QUE VAI RECEBER A CONFIRMAÇÃO DE NOVO CADASTRO  
class EmailNotificacao(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    
class BannerAula(models.Model):
    imagem = models.ImageField(upload_to='banners/aulas/')
    categoria = models.CharField(
        max_length=20,
        choices=[
            ('terra_santa', 'Terra Santa'),
            ('treinamento', 'Treinamento Empresarial'),
            ('dubai', 'Dubai'),
            ('eua', 'Estados Unidos'),
        ]
    )

    def __str__(self):
        return f'Banner Aula - {self.categoria}'


class BannerRoteiro(models.Model):
    banner_pc = models.ImageField(
        upload_to='banners/roteiros/',
        help_text="1920x500 para desktop e tablet",
        blank=True,
        null=True
    )
    banner_mobile = models.ImageField(
        upload_to='banners/roteiros/',
        help_text="480x720 para celular",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Banner Roteiro"


class MaterialDownload(models.Model):
    titulo = models.CharField(max_length=100)
    arquivo = models.FileField(upload_to='downloads/')
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class BannerDownload(models.Model):
    imagem = models.ImageField(upload_to='banners/downloads/')

    def __str__(self):
        return 'Banner Download'


class BannerManual(models.Model):
    imagem = models.ImageField(upload_to='banners/manuais/')

    def __str__(self):
        return 'Banner Manual'


class BannerProduto(models.Model):
    imagem = models.ImageField(upload_to='banners/produtos/')

    def __str__(self):
        return 'Banner Produto'


class BannerFornecedor(models.Model):
    banner_pc = models.ImageField(
        upload_to='banners/fornecedores/',
        help_text="1920x500 para desktop e tablet",
        blank=True,
        null=True
    )
    banner_mobile = models.ImageField(
        upload_to='banners/fornecedores/',
        help_text="480x720 para celular",
        blank=True,
        null=True
    )

    def __str__(self):
        return "Banner Fornecedores"
