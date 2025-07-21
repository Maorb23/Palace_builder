"""
ASGI config for palace_builder project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

key_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'OpenAI_key.txt')
if os.path.exists(key_path):
    with open(key_path) as f:
        os.environ['OPENAI_API_KEY'] = f.read().strip()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'palace_builder.settings')

application = get_asgi_application()
