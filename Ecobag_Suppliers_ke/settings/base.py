from pathlib import Path
from decouple import config

import smtplib
from email.mime.text import MIMEText

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'basket.apps.BasketConfig',
    'store.apps.StoreConfig',
    'orders.apps.OrdersConfig',
    'brands.apps.BrandsConfig',
    'supply.apps.SupplyConfig',
    'delivery.apps.DeliveryConfig',
    'widget_tweaks',
    'djmoney',
    'shipping',
    'finance',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Ecobag_Suppliers_ke.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.views.categories',
                'basket.context_processors.basket',
                'orders.context_processors.order_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ecobag_Suppliers_ke.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True




# # # settings.py
import moneyed
from moneyed import CURRENCIES, Currency

DEFAULT_CURRENCY = 'KES'

# CURRENCIES['KES'] = Currency(code='KES', name='Kenyan Shilling')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
# Base url to serve media files
MEDIA_URL = '/media/'

# Path where media is stored
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'


# testing stmp
# smtp_host = 'smtp.gmail.com'
# smtp_port = 587
# sender_email = 'peterfamous418@gmail.com'
# sender_password = 'sbvnirlqfgirrixq'
# recipient_email = 'peterfamous418@gmail.com'

# Create a connection to the SMTP server
# server = smtplib.SMTP(smtp_host, smtp_port)
# server.starttls()

# Login to the SMTP server
# server.login(sender_email, sender_password)

# Compose the email message
# message = MIMEText('This is a test email.')
# message['Subject'] = 'Test Email'
# message['From'] = sender_email
# message['To'] = recipient_email

# Send the email
# server.sendmail(sender_email, recipient_email, message.as_string())

# Close the SMTP connection
# server.quit()

# SMTP configuration
EMAIL_BACKEND = 'django.core.mail.console.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'peterfamous418@gmail.com'
DEFAULT_FROM_EMAIL = 'peterfamous418@gmail.com'
EMAIL_HOST_PASSWORD = 'sbvnirlqfgirrixq'
PASSWORD_RESET_EMAIL_TEMPLATE = 'accounts/password_reset_email.html'
PASSWORD_RESET_DONE_TEMPLATE = 'accounts/password_reset_done.html'
PASSWORD_RESET_CONFIRM_TEMPLATE = 'accounts/password_reset_confirm.html'
PASSWORD_RESET_COMPLETE_TEMPLATE = 'accounts/password_reset_complete.html'

STRIPE_ENDPOINT_SECRET = 'whsec_myIuLuukACB4Mo9HQH)ZyqgOeEc4yYov'