from aiogram.fsm.state import StatesGroup, State

class WaitUserInput(StatesGroup):
    """
    Определяет состояние FSM (Finite State Machine) для ожидания ввода пользователя.

    Этот состояние будет использоваться для управления диалогом с пользователем,
    когда пользователь должен ввести номер кресла.

    Attributes:
        user_input (State): Состояние ожидания ввода пользователя.
    """
    user_input = State()
