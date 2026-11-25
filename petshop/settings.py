"""
Configurações do projeto Django "petshop".

Gerado pelo 'django-admin startproject' (Django 3.0.3).

Documentação:
- Visão geral: https://docs.djangoproject.com/en/3.0/topics/settings/
- Lista completa de configurações: https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from dotenv import load_dotenv

# Diretório raiz do projeto (a pasta onde fica o manage.py).
# Use-o para montar caminhos: os.path.join(BASE_DIR, 'pasta', 'arquivo').
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carrega as variáveis do arquivo .env (na raiz do projeto) para o ambiente.
# Isso precisa acontecer ANTES de qualquer os.environ ser lido abaixo.
load_dotenv(os.path.join(BASE_DIR, '.env'))


# ---------------------------------------------------------------------------
# Segurança
# Checklist do deploy: https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
# ---------------------------------------------------------------------------

# Chave usada pelo Django para assinar sessões, cookies e tokens.
# Nunca deixe o valor no código: ele vem da variável de ambiente SECRET_KEY.
# Se a variável não existir, o projeto falha ao iniciar (comportamento desejado).
SECRET_KEY = os.environ['SECRET_KEY']

# Modo de depuração: mostra páginas de erro detalhadas.
# O padrão é False (seguro); ative apenas em desenvolvimento, via .env.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Domínios que podem servir a aplicação, separados por vírgula na variável
# de ambiente. Ex.: ALLOWED_HOSTS=localhost,127.0.0.1,meusite.com
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get('ALLOWED_HOSTS', '').split(',')
    if host.strip()
]


# ---------------------------------------------------------------------------
# Aplicações e middlewares
# ---------------------------------------------------------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps de terceiros
    'crispy_forms',
    'crispy_bootstrap4',
    # Apps do projeto
    'pets',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Módulo que contém as rotas (URLs) principais do projeto.
ROOT_URLCONF = 'petshop.urls'


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Pastas extras de templates (além das pastas "templates" de cada app).
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Ponto de entrada WSGI usado por servidores de produção (gunicorn, uwsgi...).
WSGI_APPLICATION = 'petshop.wsgi.application'


# ---------------------------------------------------------------------------
# Banco de dados
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# ---------------------------------------------------------------------------

# SQLite é suficiente para desenvolvimento. Em produção, considere
# PostgreSQL ou MySQL.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# ---------------------------------------------------------------------------
# Validação de senhas
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
# ---------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    # Impede senhas parecidas com os dados do usuário (nome, e-mail...).
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # Exige um tamanho mínimo (8 caracteres por padrão).
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # Bloqueia senhas muito comuns (ex.: "123456", "password").
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    # Impede senhas formadas apenas por números.
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ---------------------------------------------------------------------------
# Internacionalização
# https://docs.djangoproject.com/en/3.0/topics/i18n/
# ---------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

# Habilita o sistema de tradução do Django.
USE_I18N = True

# Armazena datas/horas com fuso horário (recomendado).
USE_TZ = True


# ---------------------------------------------------------------------------
# Arquivos estáticos e de mídia
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# ---------------------------------------------------------------------------

# Estáticos: CSS, JavaScript e imagens do próprio projeto.
STATIC_URL = '/static/'

# Mídia: arquivos enviados pelos usuários (uploads).
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')