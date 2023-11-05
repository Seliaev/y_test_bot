
from typing import Dict
from fivesim import FiveSim
from core.settings import settings

class ExampleNumber():
    """
    Класс для управления номером от 5sim.

    """
    API_KEY = settings.fivesim.api_key
    country = 'russia'
    product = 'other'
    operator = 'any'
    client = FiveSim(api_key=API_KEY, proxy=None)


    def get_balance(self) -> str:
        """
        Получает баланс акканта с сервиса.

        Returns:
            str: Баланс аккаунта в валюте аккаунта.
        """
        balance = self.client.get_balance()
        return balance['balance']

    def get_price_servise(self) -> Dict:
        """
        Получает цены на номера сервиса в стране.

        Returns:
            Dict: Словарь с ценой одного номера, количеством номеров и рейтингом оператора на сервисе.
        """

        def find_operator_with_min_cost_and_count(data: Dict[str, Dict]) -> Dict:
            """
            Находит оператора с минимальной стоимостью и ненулевым количеством номеров.

            Args:
                data (Dict[str, Dict]): Словарь с данными операторов.

            Returns:
                Dict: Словарь с ценой одного номера, количеством номеров и рейтингом оператора на сервисе.
            """
            min_cost = float('inf')
            min_cost_operator = None

            for operator, operator_data in data.items():
                if 'cost' in operator_data and 'count' in operator_data and operator_data['count'] > 0:
                    cost = operator_data['cost']
                    if cost < min_cost:
                        min_cost = cost
                        min_cost_operator = operator
            return data[min_cost_operator]

        prices = self.client.price_requests_by_country_and_product(country=self.country, product=self.product)
        rersult = find_operator_with_min_cost_and_count(prices[self.country][self.product])
        return rersult

    def get_num(self) -> Dict:
        """
        Получает номер телефона из сервиса.

        Returns:
            Dict: Словарь с данными по заказу.
            Ниже пример ответа.

            {'id': 521948864,
                  'phone': '+79154214682',
                  'operator': 'mts',
                  'product': 'other',
                  'price': 6,
                  'status': 'PENDING',
                  'expires': '2023-11-05T12:28:11.059546776Z',
                  'sms': None,
                  'created_at': '2023-11-05T12:13:11.059546776Z',
                  'country': 'russia'}

        """
        result = self.client.buy_number(country=self.country, product=self.product, operator=self.operator)
        return result

    def close_num(self, order_id: int) -> bool:
        """
        Закрывает заказ номер телефона из сервиса.

        Returns:
            bool
        """
        result = self.client.cancel_order(order_id=str(order_id))
        if result['status'] == 'CANCELED':
            return True
        else:
            return False

    def wait_code(self, order_id: int) -> str | None | bool:
        """
        Ожидает получение кода подтверждения для номера.

        Пример полного ответа ниже.

        [{
        'created_at': '2023-11-05T13:05:47.033592Z',
        'date': '2023-11-05T13:05:41Z',
        'sender': 'YAMAGUCHI',
        'text': 'Ваш проверочный код: 2784',
        'code': '2784'
        }]

        Returns:
            str: Код подтверждения.
        """
        try:
            result = self.client.check_order(order_id=str(order_id))
            if result['sms']:
                return result['sms'][0]['code']
            else: return None
        except Exception as e:
            return False


