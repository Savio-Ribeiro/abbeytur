from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from allauth.account.forms import SignupForm
from .models import Operadora, EmailNotificacao
import requests
import re
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm

class OptionalPasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove o "required" de todos os campos
        for field in self.fields.values():
            field.required = False

# 🔢 Validação matemática do CNPJ
def validar_cnpj(cnpj):
    cnpj = re.sub(r'[^0-9]', '', cnpj)

    if len(cnpj) != 14 or cnpj in (c * 14 for c in "1234567890"):
        raise ValidationError('CNPJ inválido.')

    def calcular_digito(cnpj, peso):
        soma = sum(int(c) * p for c, p in zip(cnpj, peso))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    peso1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    peso2 = [6] + peso1

    digito1 = calcular_digito(cnpj[:12], peso1)
    digito2 = calcular_digito(cnpj[:12] + digito1, peso2)

    if cnpj[-2:] != digito1 + digito2:
        raise ValidationError('CNPJ inválido.')


# 🔍 Validação via Receita Federal
def validar_cnpj_na_receita(cnpj):
    cnpj = re.sub(r'[^0-9]', '', cnpj)
    url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ERROR':
                raise ValidationError(f"CNPJ inválido na Receita: {data.get('message')}")
            if data.get('situacao') != 'ATIVA':
                raise ValidationError(f"CNPJ encontrado, mas está {data.get('situacao')}")
            return data
        else:
            raise ValidationError('Erro ao consultar a Receita. Tente novamente.')
    except Exception:
        raise ValidationError('Erro na conexão com a Receita. Tente novamente.')


# 📄 Formulário de Cadastro
class OperadoraRegistrationForm(SignupForm):
    # Dados da Empresa
    cnpj = forms.CharField(
        max_length=18,
        label='CNPJ',
        validators=[validar_cnpj]
    )
    razao_social = forms.CharField(max_length=100)
    nome_fantasia = forms.CharField(max_length=100)
    data_abertura = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    cep = forms.CharField(max_length=9)
    numero = forms.CharField(max_length=10)
    complemento = forms.CharField(max_length=50, required=False)
    logradouro = forms.CharField(max_length=150)
    bairro = forms.CharField(max_length=100)
    cidade = forms.CharField(max_length=100)
    uf = forms.CharField(max_length=2)

    site = forms.URLField(required=False)
    facebook = forms.URLField(required=False)
    instagram = forms.URLField(required=False)
    fonte_conhecimento = forms.ChoiceField(choices=Operadora.FONTE_CONHECIMENTO_CHOICES)
    logomarca = forms.ImageField(required=False)

    # Dados do Representante Legal
    nome_representante = forms.CharField(max_length=100)
    email_representante = forms.EmailField()
    email_confirm = forms.EmailField(label="Confirme seu e-mail")
    
    telefone_regex = RegexValidator(
        regex=r'^\(\d{2}\)\s?\d{4,5}-\d{4}$',
        message='Formato válido: (99) 9999-9999 ou (99) 99999-9999'
    )

    telefone_comercial1 = forms.CharField(max_length=15, validators=[telefone_regex])
    telefone_comercial2 = forms.CharField(max_length=15, required=False, validators=[telefone_regex])
    celular_representante = forms.CharField(max_length=15, validators=[telefone_regex])

    data_nascimento_representante = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar Senha'
        self.fields['email'].label = 'E-mail (será usado para login)'

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control rounded-pill'})

    def clean(self):
        cleaned_data = super().clean()
        cnpj = cleaned_data.get('cnpj')
        email = cleaned_data.get('email')
        email_confirm = cleaned_data.get('email_confirm')

        if email and email_confirm and email != email_confirm:
            self.add_error("email_confirm", "Os e-mails não coincidem.")

        if cnpj:
            try:
                dados_receita = validar_cnpj_na_receita(cnpj)

                if not cleaned_data.get('razao_social'):
                    cleaned_data['razao_social'] = dados_receita.get('nome', '')
                if not cleaned_data.get('nome_fantasia'):
                    cleaned_data['nome_fantasia'] = dados_receita.get('fantasia', dados_receita.get('nome', ''))
                if not cleaned_data.get('logradouro'):
                    cleaned_data['logradouro'] = dados_receita.get('logradouro', '')
                if not cleaned_data.get('bairro'):
                    cleaned_data['bairro'] = dados_receita.get('bairro', '')
                if not cleaned_data.get('cidade'):
                    cleaned_data['cidade'] = dados_receita.get('municipio', '')
                if not cleaned_data.get('uf'):
                    cleaned_data['uf'] = dados_receita.get('uf', '')

            except ValidationError:
                pass

        return cleaned_data

    def save(self, request):
        user = super().save(request)

        # ✅ Verifica se o e-mail já foi confirmado
        email_address = user.emailaddress_set.first()
        ativo = email_address.verified if email_address else False

        operadora = Operadora.objects.create(
            usuario=user,
            cnpj=self.cleaned_data['cnpj'],
            razao_social=self.cleaned_data['razao_social'],
            nome_fantasia=self.cleaned_data['nome_fantasia'],
            data_abertura=self.cleaned_data['data_abertura'],
            cep=self.cleaned_data['cep'],
            numero=self.cleaned_data['numero'],
            complemento=self.cleaned_data['complemento'],
            site=self.cleaned_data['site'],
            facebook=self.cleaned_data['facebook'],
            instagram=self.cleaned_data['instagram'],
            fonte_conhecimento=self.cleaned_data['fonte_conhecimento'],
            logomarca=self.cleaned_data['logomarca'],
            nome_representante=self.cleaned_data['nome_representante'],
            email_representante=self.cleaned_data['email_representante'],
            telefone_comercial1=self.cleaned_data['telefone_comercial1'],
            telefone_comercial2=self.cleaned_data['telefone_comercial2'],
            celular_representante=self.cleaned_data['celular_representante'],
            data_nascimento_representante=self.cleaned_data['data_nascimento_representante'],
            logradouro=self.cleaned_data['logradouro'],
            bairro=self.cleaned_data['bairro'],
            cidade=self.cleaned_data['cidade'],
            uf=self.cleaned_data['uf'],
            ativo=ativo,  # ✅ já define se vai ficar ativo ou não
        )

        emails = EmailNotificacao.objects.values_list('email', flat=True)
        if emails:
            send_mail(
                subject='Novo cadastro de operadora',
                message=f'Nova operadora cadastrada:\n\n'
                        f'Nome Fantasia: {operadora.nome_fantasia}\n'
                        f'E-mail do representante: {operadora.email_representante}\n'
                        f'CNPJ: {operadora.cnpj}',
                from_email='corporativo@abbeytravel.com.br',
                recipient_list=list(emails),
                fail_silently=True,
            )

        return user

class OperadoraUpdateForm(forms.ModelForm):
    class Meta:
        model = Operadora
        exclude = ['usuario', 'data_cadastro', 'ativo']  # ou liste os campos desejados

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control rounded-pill'})
