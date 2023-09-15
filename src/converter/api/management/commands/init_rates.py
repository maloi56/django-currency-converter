import xml.etree.ElementTree as ET

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    ''' Первоначальная инициализация текущих курсов валют '''

    help = 'Init current currency info'

    def handle(self, *args, **kwargs):
        response = requests.get(settings.REQUEST_URL)
        cache.set('RUB', {'nominal': 1, 'value': 1}, timeout=3600 * 24)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            for valute in root.findall('Valute'):
                key = valute.find("CharCode").text
                value = {'nominal': float(valute.find("Nominal").text.replace(',', '.')),
                         'value': float(valute.find("Value").text.replace(',', '.'))}
                cache.set(key, value, timeout=3600 * 24)

        self.stdout.write('Current currency has updated')
