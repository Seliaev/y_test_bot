import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from core.backend.magic_number_for_example import ExampleNumber as example_number
from selenium.common.exceptions import NoSuchElementException


class TestBot:
    def __init__(self, data):
        """
        Инициализирует объект TestBot.
        Тестирование функции регистрации через бота.

        Args:
            - data: тестовые данные из magic_data_for_example.py
            - example_number: номер примера (присваивается вызовом функции example_number()).
            - buttons: словарь, содержащий селекторы кнопок для разных состояний.

        Returns:
            TestBot: Объект класса TestBot.
        """
        self.data = data
        self.example_number = example_number()
        self.buttons = {
    'free': '//button[@id="submit" and @name="submit" and @class="button button--accent"]',
    'registration': '//button[@id="submit" and @name="submit" and @class="g-recaptcha button button--send"]',
    'agree': '//button[@id="submit" and @name="submit" and @class="button button--send"]',

}

    async def open_test(self, code_yamaguchi: str) -> bool:
        """
        Открывает тестовую веб-страницу и выполняет проверку наличия элемента "alertMessage".

        Args:
            code_yamaguchi (str): Код rhtckf yamaguchi для посещения соответствующей страницы.

        Returns:
            bool: Возвращает True, если элемент "alertMessage" не найден и тестовая страница успешно загружена.
                  Возвращает False, если элемент "alertMessage" найден или произошла ошибка при загрузке страницы.
        """
        self.driver = webdriver.Chrome()
        self.driver.get(f"https://yamaguchi-massage.ru/pay/{code_yamaguchi}/1")
        try:
            if self.driver.find_element(By.ID, "alertMessage"):
                self.driver.quit()
                return False
        except NoSuchElementException:
            await asyncio.sleep(1)


    async def click_button(self, name_button) -> None:
        """
        Нажимает на кнопку с заданным именем на веб-странице.

        Args:
            name_button (str): Имя кнопки, которую необходимо нажать. Имя должно соответствовать ключу в словаре buttons.

        """
        free_button = self.driver.find_element(By.XPATH, self.buttons[name_button])
        free_button.click()
        await asyncio.sleep(1)

    async def enter_name(self) -> None:
        """
        Вводит полное имя в поле ввода на веб-странице.
        """
        name_input = self.driver.find_element(By.ID, "name")
        name_input.send_keys(self.data['full_name'])

    async def enter_email(self) -> None:
        """
        Вводит email в поле ввода на веб-странице.
        """
        email_input = self.driver.find_element(By.ID, "email")
        email_input.send_keys(self.data['email'])

    async def enter_phone_number(self) -> None:
        """
        Вводит номер телефона в поле ввода на веб-странице.
        Номер телефона получает из сервиса 5SIM.
        """
        self.phone = self.example_number.get_num()
        phone_input = self.driver.find_element(By.ID, "phone")
        phone_input.send_keys(self.phone['phone'])
        await asyncio.sleep(1)

    async def click_register_button(self):
        """
        Нажимает на кнопку "Зарегистрироваться" на веб-странице.
        """
        reg_button = self.driver.find_element(By.LINK_TEXT, "Зарегистрироваться")
        reg_button.click()
        await asyncio.sleep(1)

    async def wait_and_enter_sms(self) -> None:
        """
        Ожидает получения SMS-кода и вводит его в соответствующее поле на веб-странице.
        """
        while True:
            sms = self.example_number.wait_code(order_id=self.phone['id'])
            if not sms:
                await asyncio.sleep(3)  # Подождать 3 секунды перед повторной попыткой
            else:
                sms_input = self.driver.find_element(By.ID, "verificationCode")
                sms_input.send_keys(sms)
                break

    async def screenshot(self, name_screenshot: str) -> None:
        """
        Создает снимок экрана (скриншот) и сохраняет его в файл с указанным именем.

        Args:
            name_screenshot (str): Дополнение к имени файла для сохранения скриншота.
        """
        await asyncio.sleep(2)
        self.driver.save_screenshot(f"screenshot_{name_screenshot}.png")

    def close_browser(self):
        """
        Закрывает браузер и освобождает ресурсы.
        """
        self.driver.quit()





