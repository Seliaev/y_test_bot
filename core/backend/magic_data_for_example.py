from typing import Dict
import aiohttp


async def get_example_data() -> Dict or bool:
    """
    Получает тестовые данные о несуществующем человеке из fakerapi.

    Returns:
        dict or False: Словарь с тестовыми данными о несуществующем человеке, включая полное имя и адрес электронной почты,
        или False в случае ошибки.
    """
    url = "https://fakerapi.it/api/v1/persons?_quantity=1"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'data' in data and len(data['data']) > 0:
                        person_data = data['data'][0]
                        full_name = f"{person_data['firstname']} {person_data['lastname']}"
                        return {
                            "full_name": full_name,
                            "email": person_data['email']
                        }
                return False
    except Exception as e:
        return False
