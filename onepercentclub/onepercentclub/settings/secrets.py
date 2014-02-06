"""
secrets.py

Add passwords, API keys and other secrets in this file.
"""

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'IRV+kBYsfdgkshd09874tjgfj77bjksgfjk8KJB(*fdjk'


# Database authentication
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'onepercentsite',
        'USER': 'gannetson',
        'PASSWORD': 'l3tm31n'
    }
}


COWRY_DOCDATA_MERCHANT_NAME = '1procentclub_nw'
COWRY_DOCDATA_TEST_MERCHANT_PASSWORD = 'pH2spEPe'

IPAY_VENDOR_ID = '1045'

SEPA = {
    'iban': 'NL45RABO0132207044',
    'bic': 'RABONL2U',
    'name': '1%CLUB',
    'id': 'KvK 34267895'  # KvK
}


COWRY_DOCDATA_FEES = {
    'transaction_fee': 0.20,
    'IDEAL': 0.35,
    'DIRECT_DEBIT': 0.14,
    'VISA': '2.75%',
    'MASTERCARD': '2.75%',
}

COWRY_DOCDATA_LEGACY_FEES = {
    'transaction_fee': 0.25,
    'ideal-rabobank-1procentclub_nl': 0.50,
    'ing-ideal-1procentclub_nl': 0.45,
    'ideal-ing-1procentclub_nl': 0.45,
    'omnipay-ems-visa-1procentclub_nl': '2.95%',
    'omnipay-ems-mc-1procentclub_nl': '2.95%',
    'directdebitnc-online-nl': 0.14,
    'directdebitnc2-online-nl': 0.14,
    'system-banktransfer-nl': 0.14,
}

COWRY_DOCDATA_LEGACY_MERCHANT_NAME = '1procentclub_nl'
COWRY_DOCDATA_LEGACY_LIVE_MERCHANT_PASSWORD = 'sX3n8Kt'



# FACEBOOK_APP_ID = '136522113028441'
# FACEBOOK_API_SECRET = 'd7e42dd3a60c072e543b0b5b58a9463c'


FACEBOOK_APP_ID = '623204061040531'
FACEBOOK_API_SECRET = '67ee18066d72d6c5145d2d1dc03014f8'



