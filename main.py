import asyncio


from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from core.handlers.basic import get_start, get_help, restart_bot, get_test, process_user_input
from core.middlewares.mw_backend import Middleware
from core.settings import settings
from core.states.answer_user import WaitUserInput
from core.utils.commands import set_commands
from core.backend.test_utils import TestBot
from core.backend.magic_data_for_example import get_example_data
from core.states.engine_test import EngineTets
from aiogram.fsm.state import default_state



async def assert_start(bot: Bot) -> None:
    """
    Отправляет команду на установку команд бота и сообщение об запуске бота администратору.
    """
    await set_commands(bot)
    await bot.send_message(settings.bots.id_admin, 'Бот запущен')


async def assert_stop(bot: Bot) -> None:
    """
    Отправляет сообщение об остановке бота администратору.
    """
    await bot.send_message(settings.bots.id_admin, 'Бот остановлен')


async def handle_test_operation() -> None:
    """
    Обрабатывает операцию тестирования.

    - Получает данные для тестирования с помощью функции get_example_data().
    - Если полученные данные не равны False, инициализирует объект EngineTets.test_bot
      с данными, полученными от get_example_data().
    """
    example_data = await get_example_data()
    if example_data is not False:
        EngineTets.test_bot = TestBot(data=example_data)

async def handle_bot_operations() -> None:
    """
    Обрабатывает операции, связанные с ботом.

    Инициализирует бота, устанавливает обработчики сообщений и запускает бесконечное ожидание новых сообщений.
    """
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(assert_start)
    dp.shutdown.register(assert_stop)

    dp.message.register(restart_bot, Command(commands='restart'), ~StateFilter(default_state))
    dp.message.register(get_start, Command(commands='start'), StateFilter(default_state))
    dp.message.register(get_help, Command(commands='help'), StateFilter(default_state))
    dp.message.register(get_test, Command(commands='test'), StateFilter(default_state))

    dp.message.register(process_user_input, StateFilter(WaitUserInput.user_input))

    dp.message.middleware(Middleware())


    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()




async def main() -> None:
    """
    Основная функция.

    Запускает обработку операций с ботом и тест регистрации.

    """

    await asyncio.gather(
        handle_test_operation(),
        handle_bot_operations()
    )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
