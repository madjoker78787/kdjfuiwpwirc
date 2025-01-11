import time
from datetime import datetime, timedelta

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser import driver_browser
from helper import logger, generate_telegram_url, update_time, get_data
from settings_bots import lst_bots


class Bot:
    def __init__(self, session_id):
        self.driver = None
        self.session_name = ""
        self.bot_name = ""
        self.session_id = session_id
        self.url = ""

    def enter(self, retry=0):
        url = generate_telegram_url(self.url)
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "popup-button.btn.primary.rp"))
            )
        except TimeoutException:
            logger.warning(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                           f"<fg #ffd635>{self.bot_name} | перезагрузка </fg #ffd635>#{retry}")
            return self.enter(retry=retry + 1)
        time.sleep(0.3)
        launch_btn = self.driver.find_elements(By.CLASS_NAME, "popup-button.btn.primary.rp")
        for launch in launch_btn:
            if "LAUNCH" in launch.text:
                launch.click()
                break

        try:
            WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            f = self.driver.find_element(By.TAG_NAME, "iframe")
            src = f.get_attribute("src").split("7.10")
            self.driver.execute_script("arguments[0].setAttribute('src', arguments[1]);", f,
                                       f"{src[0]}8.0{src[1]}")
        except TimeoutException:
            logger.warning(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                           f"<fg #ffd635>{self.bot_name} | перезагрузка </fg #ffd635>#{retry}")
            self.driver.switch_to.default_content()
            return self.enter(retry=retry + 1)
        logger.success(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                       f"зашел в бота <fg #898d90>{self.bot_name}</fg #898d90>")
        return True

    def add_bot(self):
        if self.enter():
            time.sleep(5)
            logger.success(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                           f"бот <fg #898d90>{self.bot_name}</fg #898d90> добавлен")
            self.driver.quit()

    def bot_run(self):
        for bot_name, bot_info in lst_bots.items():
            get_my_data = get_data(self.session_id, bot_info['table_name'])
            if datetime.now() > get_my_data[3] + timedelta(minutes=bot_info['delay']):
                if callable(bot_info['function']):
                    self.session_name = get_my_data[1]
                    self.bot_name = bot_name
                    self.url = bot_info['url']

                    self.driver = driver_browser(user_folder=self.session_name, port_=get_my_data[2])
                    logger.success(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                                   f"запуск бота <fg #898d90>{self.bot_name}</fg #898d90>")
                    if self.enter():
                        result = bot_info['function'](self.driver)
                        if result:
                            update_time(id_=self.session_id, table_name=bot_info['table_name'])
                            logger.success(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                                           f"закончил работу")