"""
Django settings for viagens project - Configuração testada e funcional
"""

import os
from pathlib import Path
import django.core.mail.backends.smtp
import django.core.mail

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== CONFIGURAÇÕES BÁSICAS ====================
SECRET_KEY = 'django-insecure-$5(8s)vhstc-o*7vh@u=4m=ws%3&$q@)^d2ebg(&p&vjksz8xs'
DEBUG = True
ALLOWED_HOSTS = ['*']

JAZZMIN_SETTINGS = {
    "site_title": "AbbeyTur Admin",
    "site_header": "Painel Administrativo AbbeyTur",
    "site_brand": "AbbeyTur",
    "welcome_sign": "Bem-vindo ao Painel AbbeyTur",
    "search_model": ["operadora.Operadora", "operadora.VideoAula"],
    "topmenu_links": [
        {"name": "Site", "url": "/", "new_window": True},
    ],
    "hide_apps": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "operadora.Operadora": "fas fa-building",
        "operadora.Fornecedor": "fas fa-handshake",
    },
}

# ==================== APPS INSTALADOS ====================
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    'core',
    'operadora.apps.OperadoraConfig',
    'crispy_forms',
    'crispy_bootstrap5',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'localflavor',    
]

ADMIN_REORDER = [
    {
        'app': 'operadora',
        'label': '🏠 HOME',
        'models': [
            {'model': 'operadora.Slide', 'label': 'Slides'},
            {'model': 'operadora.BoxProduto', 'label': 'Box produtos'},
            {'model': 'operadora.Unidade', 'label': 'Unidades'},
            {'model': 'operadora.EmailNotificacao', 'label': 'Email notificações'},
        ]
    },
    {
        'app': 'operadora',
        'label': '🎓 AULAS',
        'models': [
            {'model': 'operadora.VideoAula', 'label': 'Aulas'},
            {'model': 'operadora.BannerAula', 'label': 'Incluir banner'},
        ]
    },
    {
        'app': 'operadora',
        'label': '📄 ROTEIROS',
        'models': [
            {'model': 'operadora.Roteiro', 'label': 'Incluir Roteiro'},
            {'model': 'operadora.BannerRoteiro', 'label': 'Incluir banner'},
        ]
    },
    {
        'app': 'operadora',
        'label': '🛒 DOWNLOADS',
        'models': [
            {'model': 'operadora.MaterialDownload', 'label': 'Incluir material'},
            {'model': 'operadora.BannerDownload', 'label': 'Incluir banner'},
        ]
    },
    {
        'app': 'operadora',
        'label': '📘 MANUAIS',
        'models': [
            {'model': 'operadora.BannerManual', 'label': 'Incluir banner'},
        ]
    },
    {
        'app': 'operadora',
        'label': '🛍️ PRODUTOS',
        'models': [
            {'model': 'operadora.Produto', 'label': 'Produtos'},
            {'model': 'operadora.BannerProduto', 'label': 'Incluir banner'},
        ]
    },
    {
        'app': 'operadora',
        'label': '🤝 FORNECEDORES',
        'models': [
            {'model': 'operadora.Fornecedor', 'label': 'Fornecedores'},
            {'model': 'operadora.BannerFornecedor', 'label': 'Incluir banner'},
        ]
    },
    {
        'app': 'operadora',
        'label': '⚙️ AGENCIAS (Usuários)',
        'models': [
            {'model': 'operadora.Operadora', 'label': 'Cadastro de Operadora'},
        ]
    },
]


# ==================== MIDDLEWARE ====================
MIDDLEWARE = [
    'utils.admin_reorder_middleware.ModelAdminReorder',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

# ==================== URLs E TEMPLATES ====================
ROOT_URLCONF = 'viagens.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

# ==================== BANCO DE DADOS ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

class HTMLEmailBackend(django.core.mail.backends.smtp.EmailBackend):
    def send_messages(self, email_messages):
        fixed_messages = []
        for message in email_messages:
            if not isinstance(message, django.core.mail.EmailMultiAlternatives):
                message = django.core.mail.EmailMultiAlternatives(
                    subject=message.subject,
                    body=message.body,
                    from_email=message.from_email,
                    to=message.to,
                    cc=message.cc,
                    bcc=message.bcc,
                    reply_to=message.reply_to,
                    headers=message.extra_headers,
                    alternatives=getattr(message, 'alternatives', []),
                )
            fixed_messages.append(message)
        return super().send_messages(fixed_messages)

# ==================== VALIDAÇÃO DE SENHA ====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==================== INTERNACIONALIZAÇÃO ====================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ==================== ARQUIVOS ESTÁTICOS E MÍDIA ====================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==================== CONFIGURAÇÕES ALLAUTH DEFINITIVAS ====================
SITE_ID = 1
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configuração testada e funcional
ACCOUNT_SIGNUP_FIELDS = None
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_FORMS = {
    'signup': 'operadora.forms.OperadoraRegistrationForm',
}

# Redirecionamentos
LOGIN_REDIRECT_URL = '/home/'
LOGOUT_REDIRECT_URL = '/accounts/logout/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/dashboard/"
#INSTALLED_APPS = "/accounts/login/"


# Configurações de templates de e-mail
ACCOUNT_ADAPTER = 'core.backends.CustomAccountAdapter'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_HTML_TEMPLATE = 'account/email/email_confirmation_message.html'
ACCOUNT_EMAIL_CONFIRMATION_TEMPLATE = 'account/email/email_confirmation_message.txt'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Abbey TUR] '
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 300  # 5 minutos
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https" if not DEBUG else "http"

# ==================== CONFIGURAÇÕES DE EMAIL ====================

EMAIL_BACKEND = 'viagens.settings.HTMLEmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_LOCALTIME = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'corporativo@abbeytravel.com.br'
EMAIL_HOST_PASSWORD = 'fvoa kmbh aspb lqwm'
DEFAULT_FROM_EMAIL = 'corporativo@abbeytravel.com.br'

# ==================== CRISPY FORMS ====================
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ==================== CONFIGURAÇÕES GERAIS ====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== CONFIGURAÇÕES PARA PRODUÇÃO ====================
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'