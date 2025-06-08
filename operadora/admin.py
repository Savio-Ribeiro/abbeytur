# admin.py
from django.contrib import admin
from .models import Slide, BoxProduto, Unidade
from .models import VideoAula
from .models import EmailNotificacao
from .models import Roteiro
from .models import Fornecedor
from .models import (
    BannerAula, BannerRoteiro, MaterialDownload,
    BannerDownload, BannerManual, BannerProduto, BannerFornecedor
)

admin.site.register(BannerAula)
admin.site.register(MaterialDownload)
admin.site.register(BannerDownload)
admin.site.register(BannerManual)
admin.site.register(BannerProduto)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'pais', 'ativo', 'website')
    list_editable = ('ativo',)
    search_fields = ('nome', 'pais')
    list_filter = ('ativo', 'pais')
    ordering = ('nome',)

@admin.register(BannerFornecedor)
class BannerFornecedorAdmin(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Roteiro)
class RoteiroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_publicacao')
    search_fields = ('titulo', 'descricao')
    fieldsets = (
        (None, {
            'fields': ('titulo', 'descricao', 'arquivo')
        }),
        ('Visual', {
            'fields': ('thumbnail', 'icone', 'banner_pc', 'banner_mobile'),
            'description': 'Campos visuais para exibição no site. Todos opcionais.'
        }),
    )


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('titulo',)

@admin.register(BoxProduto)
class BoxProdutoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo')

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(VideoAula)
class VideoAulaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'data_publicacao', 'ordem')
    list_filter = ('categoria',)
    search_fields = ('titulo', 'descricao')

@admin.register(EmailNotificacao)
class EmailNotificacaoAdmin(admin.ModelAdmin):
    list_display = ('email',)

@admin.register(BannerRoteiro)
class BannerRoteiroAdmin(admin.ModelAdmin):
    list_display = ('id',)
