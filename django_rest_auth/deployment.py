import os
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://'+os.environ['WEBSITE_HOSTNAME']]
DEBUG = False
SECRET_KEY = os.environ['MY_SECRET_KEY']

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:5173",
#     "http://localhost:5173",
#     "http://127.0.0.1:3000",
#     "http://localhost:3000",
# ]


# CSRF_TRUSTED_ORIGINS=[
#     "http://127.0.0.1:5173",
#     "http://localhost:5173",
#     "http://127.0.0.1:3000",
#     "http://localhost:3000",
# ]




STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# CONNECTION = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
# CONNECTION_STR = {pair.split('=')[0]:pair.split('=')[1] for pair in CONNECTION.split(' ')}

# DATABASES = {
#     "default": {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': CONNECTION_STR['dbname'],
#         'HOST': CONNECTION_STR['host'],
#         'USER': CONNECTION_STR['user'],
#         'PASSWORD': CONNECTION_STR['password'],
#     }
# }


DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://postgres:rLZtnuwxWoSjtxdscinZwjRiaAtWcvlv@yamanote.proxy.rlwy.net:34329/railway",
        conn_max_age=600,
        ssl_require=True
    )
}


STATIC_ROOT = BASE_DIR/'staticfiles'