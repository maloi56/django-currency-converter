import logging

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import ConvertException, CurrencyException

logger = logging.getLogger(__name__)


def get_normal_value(dct):
    return round(dct['value'] / dct['nominal'], 4)


class Currency(APIView):
    '''
        Предоставляет возможность получить курсы валют в российских рублях.

        Может принимать параметр:

            valute (str, опционально): Код валюты, для которой вы хотите получить курс (например, "USD" для долларов США).
            Если этот параметр не указан, будут возвращены курсы всех доступных валют.

        Пример запроса:

            GET api/currency?valute=USD

        Доступен только авторизованным пользователям
    '''

    def get(self, request, *args, **kwargs):
        try:
            valute = self.request.query_params.get('valute', None)
            if valute:
                value = cache.get(valute.upper())
                return Response({'result': get_normal_value(value)})

            all_data = {key: get_normal_value(value) for key, value in cache.get_many(cache.keys('*')).items()}
            return Response(all_data)
        except Exception as e:
            logger.error(CurrencyException(f'Ошибка при получении курсов валют: {e}'))
            return Response({'error': 'Invalid parameters.'}, status=status.HTTP_400_BAD_REQUEST)


class Convert(APIView):
    '''
         Предоставляет функциональность для конвертации валюты.

         Принимает три query параметра:

            from (str): Код валюты, из которой будет произведена конвертация (например, "USD" для долларов США).
            to (str): Код валюты, в которую будет произведена конвертация (например, "EUR" для евро).
            amount (float): Количество валюты, которое нужно конвертировать.

        Пример запроса:

            GET api/convert?from=USD&to=EUR&amount=100

        Доступен только авторизованным пользователям
    '''

    def get(self, request, *args, **kwargs):
        try:
            fromm = self.request.query_params.get('from', None)
            to = self.request.query_params.get('to', None)
            amount = float(self.request.query_params.get('amount', None))

            return Response({'result': self.convert_currency(fromm.upper(), to.upper(), amount)})

        except Exception as e:
            logger.error(ConvertException(f'Ошибка при конвертации: {e}'))
            return Response({'error': "Invalid parameters.'from', 'to', and 'amount' are required."},
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def convert_currency(fromm, to, amount):
        from_rate = get_normal_value(cache.get(fromm))
        to_rate = get_normal_value(cache.get(to))
        return amount * from_rate / to_rate
