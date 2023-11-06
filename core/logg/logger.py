import logging


def setup_logger(log_file: str = 'bot.log', log_level: str = 'DEBUG') -> logging:
    """
    Настраивает и возвращает объект логгера.

    Attributes:
        log_file (str): Путь к файлу журнала, в который будут записываться сообщения.
        log_level (str): Уровень журналирования (по умолчанию 'DEBUG').

    Return:
        Обьект логгера
    """
    log_level = getattr(logging, log_level) if hasattr(logging, log_level) else logging.DEBUG
    logging.basicConfig(filename=log_file, level=log_level,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)
