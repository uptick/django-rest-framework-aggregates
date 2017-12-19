from .dev import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'example.urls'

REST_FRAMEWORK.update({
    'PAGE_SIZE': 1,
})