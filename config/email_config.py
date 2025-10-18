#!/usr/bin/env python3
"""
Email Configuration for SendGrid (secure)

Reads the API key from environment variable SENDGRID_API_KEY.
Never hardcode secrets in the repo. Add SENDGRID_API_KEY to your .env file.
"""

import os

# SendGrid Configuration
EMAIL_CONFIG = {
    'provider': 'sendgrid',
    'sendgrid_api_key': os.environ.get('SENDGRID_API_KEY', ''),
    'from_email': 'tomioladunjoye@zenyai.io',
    'from_name': 'Tomi from Zenyai'
}

"""
Setup:
1) Add SENDGRID_API_KEY to your .env (see .env.template)
2) Ensure your app loads env vars (dotenv or shell export)
"""
