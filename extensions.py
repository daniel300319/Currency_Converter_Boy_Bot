import requests
import json
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(curr1: str, amount: str, curr2: str):

        if curr1 == curr2:
            raise APIException(f'Валюты совпадают: {curr1}!')

        try:
            curr1_ticker = exchanges[curr1][0]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту: {curr1}')

        try:
            curr2_ticker = exchanges[curr2][0]
        except KeyError:
            raise APIException(f'Невозможно обработать валюту: {curr2}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Невозможно обработать количество: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={curr1_ticker}&tsyms={curr2_ticker}')
        base = json.loads(r.content)[exchanges[curr2][0]]

        return base