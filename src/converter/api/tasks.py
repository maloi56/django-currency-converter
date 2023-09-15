import logging
import xml.etree.ElementTree as ET

import requests
from celery import shared_task
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


@shared_task(name='update_currency')
def update_currency():
    '''Обновление курсов валют. Заполняет redis на сутки'''

    try:
        logger.info('Task started: update_currency')
        response = requests.get(settings.REQUEST_URL)
        cache.set('RUB', {'nominal': 1, 'value': 1}, timeout=3600 * 24)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            for valute in root.findall("Valute"):
                key = valute.find("CharCode").text
                value = {'nominal': float(valute.find("Nominal").text.replace(',', '.')),
                         'value': float(valute.find("Value").text.replace(',', '.'))}

                cache.set(key, value, timeout=3600 * 24)
        logger.info('Task completed: update_currency')
    except Exception as e:
        logger.error(f'Error in linter_check: {e}')
