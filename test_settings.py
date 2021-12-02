SECRET_KEY = 'notsecretnotsecretnotsecretnotsecretnotsecret'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
]
AUTH_USER_MODEL = 'auth.user'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
DEBUG = True
STATIC_URL = '/static/'
