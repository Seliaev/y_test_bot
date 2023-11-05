from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from core.settings import settings


async def set_commands(bot: Bot) -> None:
    """
    Устанавливает команды бота.

    :param bot: Инстанс бота.
    :type bot: Bot
    """
    commands = [
        BotCommand(
            command='start',
            description='Запуск бота'
        ),
        BotCommand(
            command='help',
            description='Помощь по боту'
        ),
        BotCommand(
            command='test',
                description='Выполнить тест'
        )
    ]
    commands_admin = [
        BotCommand(
            command='restart',
            description='Перезагрузка бота'
        )
    ]
    commands_admin += commands
    await bot.set_my_commands(commands, BotCommandScopeDefault())
    await bot.set_my_commands(commands_admin, BotCommandScopeChat(chat_id=settings.bots.id_admin))
