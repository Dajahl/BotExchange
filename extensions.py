import requests
import json
from config import cur_list


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def errors_check(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f"Невозможно конвертировать одинаковые валюты в {base}.")

        try:
            quote_ticker = cur_list[quote]
        except KeyError:
            raise ConvertionException(f"Неправильно введена валюта {quote}.")

        try:
            base_ticker = cur_list[base]
        except KeyError:
            raise ConvertionException(f"Неправильно введена валюта {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Неправильно введено количество {base}.")

        r = requests.get(f"https://v6.exchangerate-api.com/v6/0edb7cda4c77fa0fe34d5e8f/pair/{base_ticker}/{quote_ticker}/{amount}")
        total_base = json.loads(r.content)['conversion_result']

        return total_base