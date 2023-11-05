import os

from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    """Класс для хранения настроек бота."""
    bot_token: str
    id_admin: int


@dataclass
class FiveSim:
    """Класс для хранения настроек FiveSim."""
    api_key: str


@dataclass
class Settings:
    """Класс для хранения всех настроек."""
    bots: Bots
    fivesim: FiveSim


def get_settings(path: str) -> Settings:
    """
    Получает настройки из файла .env.

    :param path: Путь к файлу .env.
    :type path: str

    :return: Настройки бота и 5Sim.
    :rtype: Settings
    """
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN'),
            id_admin=env.int('ID_ADMIN')
        ),
        fivesim=FiveSim(
            api_key=env.str('API_KEY'),
        )
    )


root_path = os.getcwd()
env_file_path = os.path.join(root_path, '.env')
settings = get_settings(env_file_path)

