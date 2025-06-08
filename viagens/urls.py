from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from operadora import views as operadora_views
#from allauth.account.views import LoginView, LogoutView
from allauth.account.views import LoginView
from operadora.views import custom_logout
from django.views.generic import RedirectView
from operadora.views import register

urlpatterns = [
    # Páginas públicas e restritas
    path('', operadora_views.home, name='home'),
    path('home/', operadora_views.home, name='home'),
    path('downloads/', operadora_views.downloads, name='downloads'),
    path('manuais/', operadora_views.manuais, name='manuais'),
    path('cadastro/', RedirectView.as_view(url='/accounts/signup/', permanent=False), name='register'),
    #path('cadastro/', operadora_views.register, name='register'),
    path('dashboard/', operadora_views.dashboard, name='dashboard'),
    path("register/", register, name="register"),

    # Video Aulas
    path('video-aulas/', operadora_views.VideoAulaListView.as_view(), name='video_aulas'),
    path('video-aulas/terra-santa/', operadora_views.video_terra_santa, name='video_terra_santa'),
    path('video-aulas/treinamento/', operadora_views.video_treinamento_empresarial, name='video_treinamento_empresarial'),

    # Outras listas
    path('roteiros/', operadora_views.roteiros, name='roteiros'),
    path('fornecedores/', operadora_views.FornecedorListView.as_view(), name='fornecedores'),
    path('produtos/', operadora_views.ProdutoListView.as_view(), name='produtos'),

    # Login / Logout
    path('login/', LoginView.as_view(), name='account_login'),
    #path('logout/', LogoutView.as_view(), name='account_logout'),
    path('logout/', custom_logout, name='account_logout'),

    # Cadastro (personalizado)
    #path('accounts/signup/', operadora_views.register, name='account_signup'),
    path('accounts/', include('allauth.urls')),

    # Admin
    path('admin/', admin.site.urls),

    # (Se você tiver mais urls específicas dentro de operadora)
    path('operadora/', include('operadora.urls')),
]

# Arquivos de mídia (dev only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
