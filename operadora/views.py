# operadora/views.py
from django.contrib.auth import logout
from allauth.account.models import EmailAddress
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import (
    Operadora, VideoAula, Roteiro, Fornecedor, BannerFornecedor,
    Produto, Slide, BoxProduto, Unidade
)
from .forms import OptionalPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import OperadoraRegistrationForm, OperadoraUpdateForm
from django.contrib import messages
from allauth.account.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.urls import reverse
from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings
from allauth.account.views import SignupView
from .forms import OperadoraRegistrationForm
from .models import Roteiro, BannerRoteiro

class CustomLoginView(LoginView):
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        storage = messages.get_messages(request)
        storage.used = True  # 🔕 limpa mensagens anteriores
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)

        # ✅ Após login, ativa operadora se e-mail confirmado
        user = self.request.user
        if hasattr(user, 'operadora'):
            email_obj = EmailAddress.objects.filter(user=user, email=user.email).first()
            if email_obj and email_obj.verified and not user.operadora.ativo:
                user.operadora.ativo = True
                user.operadora.save()
                print(f"✅ Operadora ativada via login para: {user.email}")

        return response

def home(request):
    slides = Slide.objects.filter(ativo=True).order_by('ordem')
    box_produtos = BoxProduto.objects.filter(ativo=True)
    produtos = Produto.objects.filter(ativo=True)
    unidades = Unidade.objects.all()

    context = {
        'slides': slides,
        'box_produtos': box_produtos,
        'produtos': produtos,
        'unidades': unidades,
    }
    return render(request, 'operadora/home.html', context)

def downloads(request):
    return render(request, 'operadora/downloads.html')

def manuais(request):
    return render(request, 'operadora/manuais.html')

def register(request):
    if request.method == 'POST':
        form = OperadoraRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request)
            return redirect('account_login')  # Ou 'dashboard' se preferir
    else:
        form = OperadoraRegistrationForm()
    
    return render(request, 'account/signup.html', {'form': form})

@login_required
@login_required
def dashboard(request):
    try:
        operadora = request.user.operadora
    except Operadora.DoesNotExist:
        messages.error(request, "Você ainda não completou seu cadastro.")
        return redirect('register')

    user = request.user

    if request.method == 'POST':
        operadora_form = OperadoraUpdateForm(request.POST, request.FILES, instance=operadora)
        email = request.POST.get("email")
        senha_antiga = request.POST.get("old_password")
        nova_senha = request.POST.get("new_password1")

        # ✅ usa o form personalizado só se campos foram preenchidos
        if senha_antiga or nova_senha:
            password_form = OptionalPasswordChangeForm(user, request.POST)
        else:
            password_form = None

        if operadora_form.is_valid():
            operadora_form.save()

            # Atualiza o e-mail, se alterado
            if email and email != user.email:
                user.email = email
                user.save()

            # Se o form de senha foi criado (usuário quis alterar)
            if password_form:
                if password_form.is_valid():
                    password_form.save()
                    update_session_auth_hash(request, password_form.user)
                else:
                    messages.error(request, "Erro ao atualizar a senha. Verifique os campos.")
                    return redirect('dashboard')

            messages.success(request, 'Dados atualizados com sucesso.')
            return redirect('dashboard')
        else:
            messages.error(request, "Erro ao salvar os dados. Verifique os campos obrigatórios.")

    else:
        operadora_form = OperadoraUpdateForm(instance=operadora)
        password_form = OptionalPasswordChangeForm(user)

    return render(request, 'dashboard.html', {
        'operadora_form': operadora_form,
        'password_form': password_form,
        'user_email': user.email,
        'operadora': operadora,
    })

#PÁGINA DAS AULAS
@login_required
def video_terra_santa(request):
    videos = VideoAula.objects.filter(categoria='terra_santa').order_by('ordem')
    return render(request, 'operadora/video-aula/terra_santa.html', {'videos': videos})

@login_required
def video_treinamento_empresarial(request):
    videos = VideoAula.objects.filter(categoria='treinamento').order_by('ordem')
    return render(request, 'operadora/video-aula/treinamento_empresarial.html', {'videos': videos})

class VideoAulaListView(LoginRequiredMixin, ListView):
    model = VideoAula
    template_name = 'operadora/video_aulas.html'
    context_object_name = 'videos'
    
    def get_queryset(self):
        categoria = self.request.GET.get('categoria', 'terra_santa')
        return VideoAula.objects.filter(categoria=categoria).order_by('ordem')


@login_required
def roteiros(request):
    roteiros = Roteiro.objects.all().order_by('data_publicacao')
    banner = BannerRoteiro.objects.last()  # Pega o mais recente

    return render(request, 'operadora/roteiros.html', {
        'roteiros': roteiros,
        'banner': banner,
    })

class FornecedorListView(LoginRequiredMixin, ListView):
    model = Fornecedor
    template_name = 'operadora/fornecedores.html'
    context_object_name = 'fornecedores'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banner'] = BannerFornecedor.objects.last()
        return context

    def get_queryset(self):
        return Fornecedor.objects.filter(ativo=True)

class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = 'operadora/produtos.html'
    context_object_name = 'produtos'
    
    def get_queryset(self):
        return Produto.objects.filter(ativo=True)
    
def custom_logout(request):
    logout(request)  # Destroi a sessão
    request.session.flush()  # Garante remoção total de cookies/sessão
    return render(request, 'operadora/logout.html')
