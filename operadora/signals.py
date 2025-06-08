from allauth.account.signals import email_confirmed
from django.dispatch import receiver
from .models import Operadora

@receiver(email_confirmed)
def ativar_operadora_apos_confirmacao_email(request, email_address, **kwargs):
    user = email_address.user
    print(f"🚀 Signal ativado corretamente para: {user.email}")
    try:
        operadora = user.operadora
        operadora.ativo = True
        operadora.save()
        print(f"✅ Acesso ativado para {user.email}")
    except Operadora.DoesNotExist:
        print(f"❌ Acesso não ativado: operadora não existe para {user.email}")

