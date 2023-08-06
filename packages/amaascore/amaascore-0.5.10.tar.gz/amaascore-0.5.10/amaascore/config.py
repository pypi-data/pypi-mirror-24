# POTENTIALLY SUPPORT MULTIPLE ENVIRONMENTS
from __future__ import absolute_import, division, print_function, unicode_literals

envs = {'local', 'dev', 'staging', 'production'}

ENVIRONMENT = 'production'
API_VERSION = 'v1.0'

LOCAL_ENDPOINT = 'http://localhost:8000'
BASE_URLS = {
    'production': 'https://api.amaas.com',
    'staging': 'https://api-staging.amaas.com',
    'dev': 'https://api-dev.amaas.com'
}

ENDPOINTS = {
    'asset_managers': 'assetmanager',
    'assets': 'asset',
    'books': 'book',
    'corporate_actions': 'corporateaction',
    'fundamentals': 'fundamental',
    'market_data': 'marketdata',
    'monitor': 'monitor',
    'parties': 'party',
    'transactions': 'transaction'
}

COGNITO_CLIENT_ID = '55n70ns9u5stie272e1tl7v32v'  # This is not secret - it is just an identifier

# Do not change this
COGNITO_REGION = 'us-west-2'
COGNITO_POOL = 'us-west-2_wKa82vECF'
