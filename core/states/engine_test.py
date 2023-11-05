from aiogram.fsm.state import StatesGroup, State


class EngineTets(StatesGroup):
    """
    Определяет состояние FSM (Finite State Machine) для управления тестовым ботом.

    Этот класс используется для организации состояния FSM, связанного с тестированием функциональности бота.

    Attributes:
        test_bot (State): Состояние, связанное с тестовым ботом.
    """
    test_bot = State()
