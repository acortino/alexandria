import os
import re

import environ
from django.conf import global_settings

env = environ.Env()
django_root = environ.Path(__file__) - 2

ENV_FILE = env.str("ENV_FILE", default=django_root(".env"))
if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)

# per default production is enabled for security reasons
# for development create .env file with ENV=development
ENV = env.str("ENV", "production")


def default(default_dev=env.NOTSET, default_prod=env.NOTSET):
    """Environment aware default."""
    return default_prod if ENV == "production" else default_dev


SECRET_KEY = env.str("SECRET_KEY", default=default("uuuuuuuuuu"))
DEBUG = env.bool("DEBUG", default=default(True, False))
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=default(["*"]))


# Application definition

INSTALLED_APPS = [
    "django.contrib.postgres",
    "localized_fields",
    "psqlextra",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "alexandria.core.apps.DefaultConfig",
]

if ENV == "dev":
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "alexandria.urls"
WSGI_APPLICATION = "alexandria.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": env.str("DATABASE_NAME", default="alexandria"),
        "USER": env.str("DATABASE_USER", default="alexandria"),
        "PASSWORD": env.str("DATABASE_PASSWORD", default=default("alexandria")),
        "HOST": env.str("DATABASE_HOST", default="localhost"),
        "PORT": env.str("DATABASE_PORT", default=""),
        "OPTIONS": env.dict("DATABASE_OPTIONS", default={}),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/


def parse_languages(languages):
    return [(language, language) for language in languages]


LANGUAGE_CODE = env.str("LANGUAGE_CODE", "en")
LANGUAGES = (
    parse_languages(env.list("LANGUAGES", default=["en"])) or global_settings.LANGUAGES
)

TIME_ZONE = env.str("TIME_ZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALIZED_FIELDS_EXPERIMENTAL = True


ADMIN_USERNAME = env.str("ADMIN_USERNAME", default="admin")

# Authentication
OIDC_OP_USER_ENDPOINT = env.str("OIDC_OP_USER_ENDPOINT", default=None)
OIDC_OP_TOKEN_ENDPOINT = "not supported in alexandria, but a value is needed"
OIDC_VERIFY_SSL = env.bool("OIDC_VERIFY_SSL", default=True)
OIDC_USERNAME_CLAIM = env.str("OIDC_USERNAME_CLAIM", default="sub")
OIDC_GROUPS_CLAIM = env.str("OIDC_GROUPS_CLAIM", default="alexandria_groups")
OIDC_BEARER_TOKEN_REVALIDATION_TIME = env.int(
    "OIDC_BEARER_TOKEN_REVALIDATION_TIME", default=0
)
OIDC_OP_INTROSPECT_ENDPOINT = env.str("OIDC_OP_INTROSPECT_ENDPOINT", default=None)
OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID", default=None)
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET", default=None)

DEV_AUTH_BACKEND = env.bool("DEV_AUTH_BACKEND", default=False)
OIDC_DRF_AUTH_BACKEND = (
    "alexandria.oidc_auth.authentication.DevelopmentAuthenticationBackend"
    if DEV_AUTH_BACKEND
    else "alexandria.oidc_auth.authentication.AlexandriaAuthenticationBackend"
)

# Extensions

VISIBILITY_CLASSES = env.list(
    "VISIBILITY_CLASSES", default=default(["alexandria.core.visibilities.Any"])
)

PERMISSION_CLASSES = env.list(
    "PERMISSION_CLASSES", default=default(["alexandria.core.permissions.AllowAny"])
)
VALIDATION_CLASSES = env.list("VALIDATION_CLASSES", default=[])


# Storage
MEDIA_STORAGE_SERVICE = env.str("MEDIA_STORAGE_SERVICE", default="minio")
MINIO_STORAGE_ENDPOINT = env.str("MINIO_STORAGE_ENDPOINT", default="minio:9000")
MINIO_STORAGE_ACCESS_KEY = env.str("MINIO_STORAGE_ACCESS_KEY", default="minio")
MINIO_STORAGE_SECRET_KEY = env.str("MINIO_STORAGE_SECRET_KEY", default="minio123")
MINIO_STORAGE_USE_HTTPS = env.str("MINIO_STORAGE_USE_HTTPS", default=False)
MINIO_STORAGE_MEDIA_BUCKET_NAME = env.str(
    "MINIO_STORAGE_MEDIA_BUCKET_NAME", default="alexandria-media"
)
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = env.str(
    "MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET", default=True
)
MINIO_PRESIGNED_TTL_MINUTES = env.str("MINIO_PRESIGNED_TTL_MINUTES", default=15)


# Thumbnails
ENABLE_THUMBNAIL_GENERATION = env.bool("ENABLE_THUMBNAIL_GENERATION", default=True)
THUMBNAIL_WIDTH = env.int("THUMBNAIL_WIDTH", default=None)
THUMBNAIL_HEIGHT = env.int("THUMBNAIL_HEIGHT", default=None)


REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework_json_api.pagination.JsonApiPageNumberPagination",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework_json_api.parsers.JSONParser",
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework_json_api.filters.QueryParameterValidationFilter",
        "rest_framework_json_api.filters.OrderingFilter",
        "rest_framework_json_api.django_filters.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "ORDERING_PARAM": "sort",
    "SEARCH_PARAM": "filter[search]",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework_json_api.renderers.JSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}

JSON_API_FORMAT_FIELD_NAMES = "dasherize"
JSON_API_FORMAT_TYPES = "dasherize"
JSON_API_PLURALIZE_TYPES = True


# Anonymous writing
ALLOW_ANONYMOUS_WRITE = env.bool("ALLOW_ANONYMOUS_WRITE", default=False)

if ALLOW_ANONYMOUS_WRITE:
    REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] = [
        "rest_framework.permissions.AllowAny",
    ]


def parse_admins(admins):
    """
    Parse env admins to django admins.

    Example of ADMINS environment variable:
    Test Example <test@example.com>,Test2 <test2@example.com>
    """
    result = []
    for admin in admins:
        match = re.search(r"(.+) \<(.+@.+)\>", admin)
        if not match:  # pragma: no cover
            raise environ.ImproperlyConfigured(
                'In ADMINS admin "{0}" is not in correct '
                '"Firstname Lastname <email@example.com>"'.format(admin)
            )
        result.append((match.group(1), match.group(2)))
    return result


ADMINS = parse_admins(env.list("ADMINS", default=[]))
