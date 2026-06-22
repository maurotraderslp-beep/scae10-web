"""
Django settings for scae10 project.
Generated for SCAE10 Web - Sistema de Controle de Arquivo Escolar
"""

from pathlib import Path
import os

import os
from pathlib import Path

# Adicione esta linha:
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-scae10-dev-key-change-in-production-2024'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Adicione estas linhas:
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.onrender.com',
    'https://*.pythonanywhere.com',
    'http://localhost:8000',
]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps do SCAE10
    'autenticacao',
    'alunos',
    'corredores',
    'estantes',
    'prateleiras',
    'equipamentos',
    'calendarios',
    'solicitacoes',
    'professores',
    'documentos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'scae10.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'alunos' / 'templates',
            BASE_DIR / 'corredores' / 'templates',
            BASE_DIR / 'estantes' / 'templates',
            BASE_DIR / 'prateleiras' / 'templates',
            BASE_DIR / 'equipamentos' / 'templates',
            BASE_DIR / 'calendarios' / 'templates',
            BASE_DIR / 'solicitacoes' / 'templates',
            BASE_DIR / 'professores' / 'templates',
            BASE_DIR / 'documentos' / 'templates',
        ],
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

WSGI_APPLICATION = 'scae10.wsgi.application'

# Database - Firebird 2.5
# Usando fdb (Python Firebird driver)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Firebird Connection (manual)
FIREBIRD_CONFIG = {
    'dsn': r'c:\sysflor\scae10-python\database\SCAE.FDB',
    'user': 'SYSDBA',
    'password': 'masterkey',
    'charset': 'WIN1252',
    'port': 3025,  # Firebird 2.5 usa porta 3025
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Belem'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (uploads, documentos gerados)
MEDIA_URL = '/media/'
# Pasta onde as fotos dos alunos serão salvas (dentro do projeto)
MEDIA_ROOT = BASE_DIR / 'media'

# Criar pasta se não existir
import os

e a configuração do banco e substitua por:
# Database configuration
import os

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL and 'postgresql' in DATABASE_URL:
    # Produção (PostgreSQL)
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL)
    }
elif DATABASE_URL and 'sqlite' in DATABASE_URL:
    # Teste (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Local (Firebird)
    DATABASES = {
        'default': {
            'ENGINE': 'django_firebird',
            'NAME': 'C:/SCAE10/BANCO/SCAE10.FDB',
            'USER': 'SYSDBA',
            'PASSWORD': 'masterkey',
            'HOST': 'localhost',
            'PORT': '3025',
            'OPTIONS': {
                'charset': 'WIN1252',
            }
        }
    }

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT, exist_ok=True)
    print(f"[INFO] Pasta media criada em: {MEDIA_ROOT}")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Messages
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
'whitenoise.middleware.WhiteNoiseMiddleware',