import os

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"
ALLOWED_HOSTS = (
    ["*"] if DEBUG else os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
)

INSTALLED_APPS = [
    "django.contrib.postgres",
    "paper_rag.papers",
    "paper_rag.core.model",
    "paper_rag.ingester",
]

MIDDLEWARE = ["django.middleware.common.CommonMiddleware"]
ROOT_URLCONF = "paper_rag.urls"
WSGI_APPLICATION = "paper_rag.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
MIGRATION_MODULES = {
    "model": "migrations.model",
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
USE_TZ = True
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "UNAUTHENTICATED_USER": None,
}
