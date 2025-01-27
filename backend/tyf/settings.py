import os
import datetime
from pathlib import Path
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = int(os.getenv("DEBUG", default=0))
ALLOWED_HOSTS = ["*"]

# TODO: Change to production URL
API_ULR = "http://localhost:8000"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

DEFAULT_USER_AVATAR = "/static/default_avatar_light.webp"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")


# TODO: Enable in production
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]
CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-Api-Key",
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]


AUTH_USER_MODEL = "users.User"

# Daphne
ASGI_APPLICATION = "tyf.asgi.application"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.getenv("REDIS_LOCATION")],
        },
    },
}

INSTALLED_APPS = [
    "daphne",
    "channels",
    "channels_redis",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "rest_framework_api_key",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "apps.celery_app",
    "apps.users",
    "apps.profiles",
    "apps.registry",
    "apps.categories",
    "apps.collections",
    "apps.tags",
    "apps.tye",
    "apps.posts",
    "apps.comments",
    "apps.media",
    "apps.follows",
    "apps.chats",
    "apps.notifications",
    "django_select2",
    "mdeditor",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",)


# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:8080",
]

ROOT_URLCONF = "tyf.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
        },
    },
]


# WSGI_APPLICATION = "tyf.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}


TYF_USER_VERIFICATION_KEY = "user_verification_{token}"
TYF_USER_VERIFICATION_TIMEOUT = 15 * 60

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "TIMEOUT": TYF_USER_VERIFICATION_TIMEOUT,
        },
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_LOCATION"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

CELERY_BROKER_URL = os.getenv("REDIS_LOCATION")
CELERY_RESULT_BACKEND = os.getenv("REDIS_LOCATION")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# CELERY_broker_url = "amqp://myuser:mypassword@localhost:5672/myvhost"
# result_backend = "redis://localhost:6379"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework_api_key.permissions.HasAPIKey",
    ],
    "DATE_INPUT_FORMATS": [
        "%d.%m.%Y",
    ],
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = "jwt-auth"

SIMPLE_JWT = {
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=7),
}

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Vladivostok"
USE_I18N = True
USE_TZ = True
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
X_FRAME_OPTIONS = "SAMEORIGIN"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email Configurations
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


MDEDITOR_CONFIGS = {
    "default": {
        "width": "90% ",  # Custom edit box width
        "height": 500,  # Custom edit box height
        "toolbar": [
            "undo",
            "redo",
            "|",
            "bold",
            "del",
            "italic",
            "quote",
            "ucwords",
            "uppercase",
            "lowercase",
            "|",
            "h1",
            "h2",
            "h3",
            "h5",
            "h6",
            "|",
            "list-ul",
            "list-ol",
            "hr",
            "|",
            "link",
            "reference-link",
            "image",
            "code",
            "preformatted-text",
            "code-block",
            "table",
            "datetime",
            "emoji",
            "html-entities",
            "pagebreak",
            "goto-line",
            "|",
            "help",
            "info",
            "||",
            "preview",
            "watch",
            "fullscreen",
        ],  # custom edit box toolbar
        "upload_image_formats": [
            "jpg",
            "jpeg",
            "gif",
            "png",
            "bmp",
            "webp",
        ],  # image upload format type
        "image_folder": "post_data",  # image save the folder name
        "theme": "default",  # edit box theme, dark / default
        "preview_theme": "default",  # Preview area theme, dark / default
        "editor_theme": "default",  # edit area theme, pastel-on-dark / default
        "toolbar_autofixed": True,  # Whether the toolbar capitals
        "search_replace": True,  # Whether to open the search for replacement
        "emoji": True,  # whether to open the expression function
        "tex": True,  # whether to open the tex chart function
        "flow_chart": True,  # whether to open the flow chart function
        "sequence": True,  # Whether to open the sequence diagram function
        "watch": True,  # Live preview
        "lineWrapping": False,  # lineWrapping
        "lineNumbers": False,  # lineNumbers
        "language": "en",  # zh / en / es
    }
}

SELECT2_CACHE_BACKEND = "select2"

LANGUAGE_CODE = "ru"

LANGUAGES = [
    ("ru", "Русский"),
    ("en", "English"),
]

TYE_MONGO_URL=os.getenv("TYE_MONGO_URL")