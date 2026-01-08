from pathlib import Path
import os
import json
import random
import hexoweb.exceptions as exceptions
import logging
import urllib3

urllib3.disable_warnings()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mrf1flh+i8*!ao73h6)ne#%gowhtype!ld#+(j^r*!^11al2vz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

LOCAL_CONFIG = False

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'hexoweb.apps.ConsoleConfig',
    'corsheaders',
    # "passkeys"
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

errors = ""

if os.environ.get("DB_URI"):
    import pymongo
    logging.info("检测到 DB_URI，正在连接...")
    uri = os.environ.get("DB_URI")
    try:
        # 自动从连接字符串里提取数据库名，提取不到就用 qexo
        db_name = pymongo.uri_parser.parse_uri(uri)['database']
        if not db_name: db_name = 'qexo'
    except:
        db_name = 'qexo'
        
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'ENFORCE_SCHEMA': False,
            'NAME': db_name,
            'CLIENT': {
                'host': uri,
            }
        }
    }

elif os.environ.get("MONGODB_HOST"):
    logging.info("使用环境变量中的MongoDB数据库")
    for env in ["MONGODB_HOST", "MONGODB_PORT", "MONGODB_PASS"]:
        if env not in os.environ:
            errors += f"\"{env}\" "
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'ENFORCE_SCHEMA': False,
            'NAME': 'django',
            'CLIENT': {
                'host': os.environ.get("MONGODB_HOST"),
                'port': int(os.environ.get("MONGODB_PORT")),
                'username': os.environ.get("MONGODB_USER") or "root",
                'password': os.environ.get("MONGODB_PASS"),
                'authSource': os.environ.get("MONGODB_DB") or "root",
                'authMechanism': 'SCRAM-SHA-1'
            }
        }
    }

elif os.path.exists(BASE_DIR / "configs.py"):
    import configs
    DATABASES = configs.DATABASES
    LOCAL_CONFIG = True
else:
    # 如果上面都没命中，才会报错
    errors = "数据库配置 (DB_URI 或 HOST/PORT)"

if errors:
    logging.error(f"{errors}未设置, 请查看: https://www.oplog.cn/qexo/start/build.html")
    raise exceptions.InitError(f"{errors}未设置, 请查看: https://www.oplog.cn/qexo/start/build.html")

if LOCAL_CONFIG:
    logging.info("获取本地配置文件成功, 使用本地配置部署")
    ALLOWED_HOSTS = configs.DOMAINS
else:
    logging.info("未检测到本地配置, 使用环境变量获取配置")  # Serverless部署
    ALLOWED_HOSTS = json.loads(os.environ.get("DOMAINS", False)) if os.environ.get("DOMAINS", False) else ["*"]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_AGE = 86400
