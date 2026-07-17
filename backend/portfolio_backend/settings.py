"""
Django settings for portfolio_backend project.
"""
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'contact',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portfolio_backend.urls'

WSGI_APPLICATION = 'portfolio_backend.wsgi.application'

# ─── CORS ─────────────────────────────────────────────────────
# Allow your portfolio HTML to call the API
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:5500',
    'http://localhost:5500',
    'http://127.0.0.1:5501',   # User's configured VS Code Live Server port
    'http://localhost:5501',
    'http://localhost:8080',   # Local python HTTP server
    'http://127.0.0.1:8080',
    'https://oumaelba.vercel.app', # Live Vercel frontend
]
# When deployed, add your live domain here, e.g.:
# 'https://elbaouma.github.io'

# ─── Email ────────────────────────────────────────────────────
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

if DEBUG and not MAIL_USERNAME:
    # Use console email backend during local testing if SMTP credentials are missing
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'portfolio-no-reply@localhost'
    OWNER_EMAIL = os.getenv('OWNER_EMAIL', 'admin@localhost')
else:
    EMAIL_BACKEND   = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST      = 'smtp.gmail.com'
    EMAIL_PORT      = 587
    EMAIL_USE_TLS   = True
    EMAIL_HOST_USER = MAIL_USERNAME
    EMAIL_HOST_PASSWORD = MAIL_PASSWORD
    DEFAULT_FROM_EMAIL  = MAIL_USERNAME
    OWNER_EMAIL     = os.getenv('OWNER_EMAIL', MAIL_USERNAME)

ADMIN_DASHBOARD_KEY = os.getenv('ADMIN_DASHBOARD_KEY', '40882153')

import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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
