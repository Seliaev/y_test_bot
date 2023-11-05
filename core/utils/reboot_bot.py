import sys
import os


def restart_script() -> None:
    """
    Перезапускает скрипт Python.

    Функция определяет путь к исполняемому файлу Python, текущую директорию и имя текущего скрипта.
    Затем она использует функцию `os.execv()` для перезапуска текущего скрипта Python с тем же исполняемым файлом.
    """
    python_executable = sys.executable
    root = os.getcwd()
    script_file = "main.py"
    file_path = os.path.join(root, script_file)
    os.execv(python_executable, ['python', file_path])

