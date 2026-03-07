import os
from pathlib import Path
from corsheaders.defaults import default_headers
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


#                        Production     (devs- auto switch if production env isn't found)
environment = os.getenv("ENVIRONMENT", "development")
print(environment)
if environment == "production":
    load_dotenv()
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }
    SECRET_KEY = os.getenv("DJANGO_KEY")
    DEBUG = False
    ALLOWED_HOSTS = [
        host.strip()
        for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
        if host.strip()
    ]
else:
    load_dotenv(f".env.{environment}")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }
    SECRET_KEY = os.getenv("DJANGO_KEY")
    DEBUG = True
    ALLOWED_HOSTS = [
        host.strip()
        for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
        if host.strip()
    ]

# Default settings
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "server",
]
CORS_ALLOWED_ORIGINS = [
    (x.strip() if x.strip().startswith("http") else ("https://" if environment == "production" else "http://") + x.strip()).rstrip("/")
    for x in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if x.strip()
]

# Send Mail
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_APP_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_APP_USER", "noreply.resonancese@gmail.com")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    *default_headers,
    "X-CSRFToken",
]


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server.wsgi.application"

IMGBB_API_KEY = os.getenv("API_IMG_KEY")
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": ("django.contrib.auth.password_validation.CommonPasswordValidator"),
    },
    {
        "NAME": ("django.contrib.auth.password_validation.NumericPasswordValidator"),
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "server.middleware.auth_middleware.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}

# Localization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
CORS_ALLOW_CREDENTIALS = True
# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "server.Customer"
