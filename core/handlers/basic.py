import os

from core.logg.logger import setup_logger
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from core.states.answer_user import WaitUserInput
from core.states.engine_test import EngineTets

logger = setup_logger(log_file='debug.log', log_level='DEBUG')

# Команды пользователя
async def get_start(message: Message) -> None:
    """
    Приветствует пользователя и предоставляет информацию о доступных командах.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    name = message.from_user.first_name
    await message.answer(f'Привет, {name}!\n'
                         f'Что бы узнать о командах и возможностях введи /help')


async def get_help(message: Message) -> None:
    """
    Предоставляет справочную информацию о доступных командах и функциональности бота.

    Args:
        message (Message): Объект сообщения от пользователя.
    """
    help_text = """
    Привет!
    
    👋 Что умеет бот:
        - Бот может протестировать доступность регистрации аккаунта\nна сервисе "Yamaguchi" для массажных сеансов.
    
    🚫 Нарушения и правила:
        - Пожалуйста, используйте бота только для легальных целей.
        - Использование тестовой команды разрешено только единожды.
        - Мы не поддерживаем злоупотребление или нарушение правил.
    
    📜 Команды:
        - /start - Начать взаимодействие с ботом.
        - /test - Проверить функциональность регистрации.
        - /help - Получить это сообщение с описанием.
    
    Спасибо за понимание и честное использование нашего бота! 👍
    """
    await message.answer(help_text)


async def get_test(message: Message, state: FSMContext) -> None:
    """
    Инициирует процесс тестирования функциональности регистрации на сервисе yamaguchi.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Состояние FSM (Finite State Machine) для управления диалогом.
    """
    await message.answer("! Введите номер кресла в формате - DS12345 !")
    await state.set_state(WaitUserInput.user_input)

async def process_user_input(message: Message, state: FSMContext):
    """
    Обрабатывает введенный пользователем номер кресла и выполняет тестирование функциональности регистрации.

    Args:
        message (Message): Объект сообщения от пользователя.
        state (FSMContext): Состояние FSM (Finite State Machine) для управления диалогом.
    """
    user_input = message.text
    open_test =  await EngineTets.test_bot.open_test(code_yamaguchi=user_input)
    logger.debug(f'Тест подготовлен для {user_input}')
    if open_test is not False:
        logger.debug(f'Тест запущен')
        await EngineTets.test_bot.click_button(name_button='free')
        logger.debug(f'Переход по ссылке 1 успешен')
        await EngineTets.test_bot.click_register_button()
        logger.debug(f'Переход по ссылке 2 успешен')
        await EngineTets.test_bot.enter_name()
        await EngineTets.test_bot.enter_email()
        await EngineTets.test_bot.enter_phone_number()
        logger.debug(f'Данные введены успешно')
        await EngineTets.test_bot.click_button(name_button='registration')
        logger.debug(f'Переход по ссылке 3 успешен')
        await EngineTets.test_bot.wait_and_enter_sms()
        logger.debug(f'СМС получено успешно')
        await EngineTets.test_bot.click_button(name_button='agree')
        logger.debug(f'Переход по ссылке 4 успешен')
        await EngineTets.test_bot.screenshot(name_screenshot=message.from_user.id)
        logger.debug(f'Скриншот создан успешно')
        await message.answer('! Тест успешно завершен !')
        image_path = f"screenshot_{message.from_user.id}.png"
        screenshot = FSInputFile(image_path)
        await message.answer_photo(photo=screenshot)
        os.remove(image_path)
    else:
        await message.answer("! Неудача !")
    EngineTets.test_bot.close_browser()
    logger.debug(f'Браузер закрыт')
    await state.clear()


