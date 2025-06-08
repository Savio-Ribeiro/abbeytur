# core/backends.py
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from operadora.models import Operadora  # ✅ importe seu modelo
from django.contrib import messages

class CustomAccountAdapter(DefaultAccountAdapter):
    def confirm_email(self, request, email_address):
        # Marca o e-mail como principal e verificado
        email_address.set_as_primary()
        email_address.verified = True
        email_address.save()

        # Ativa o usuário (caso esteja inativo)
        user = email_address.user
        if not user.is_active:
            user.is_active = True
            user.save()

        # ✅ Aqui você ativa a operadora também
        try:
            operadora = user.operadora
            if not operadora.ativo:
                operadora.ativo = True
                operadora.save()
                print(f"✅ Operadora ativada via adapter para {user.email}")
        except Operadora.DoesNotExist:
            print(f"❌ Operadora não encontrada para {user.email}")

        # ✅ Mensagem de sucesso
        messages.success(request, "Cadastro ativado com sucesso!")
