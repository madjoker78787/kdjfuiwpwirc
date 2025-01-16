import time
from datetime import datetime, timedelta

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

from browser import driver_browser
from helper import logger, generate_telegram_url, update_time, get_last_visit
from settings_bots import lst_bots

from proxy_list import lst

def check_bots(data):
    for bot_name, bot_info in lst_bots.items():
        get_my_data = get_last_visit(data[0], bot_info['table_name'])
        if (datetime.now() >
                datetime.strptime(get_my_data[0], "%d.%m.%Y %H:%M") +
                timedelta(minutes=bot_info['delay'])):

            driver = driver_browser(user_folder=data[1],
                           port_=data[2],
                           proxy_=lst[data[0]],
                           dev=bot_info['dev'])
            bot_ = Bot(session_id=data[0],
                         session_name=data[1],
                         driver=driver,
                         bot_name=bot_name,
                         url=bot_info['url'],
                         func=bot_info['function'])
            result = bot_.bot_run()
            if result:
                update_time(id_=data[0], table_name=bot_name)
                driver.quit()
            else:
                driver.quit()
    return

class Bot:
    def __init__(self, session_id, session_name, driver: webdriver.Chrome, bot_name, url, func):
        self.driver = driver
        self.session_id = session_id
        self.session_name = session_name

        self.bot_name = bot_name
        self.url = url
        self.func = func

    def enter(self, retry=0):
        self.driver.get("https://web.telegram.org/k/")
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
            if "launch" in launch.text.lower():
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
        frame = self.driver.find_element(By.TAG_NAME, "iframe")
        self.driver.switch_to.frame(frame)
        # return True

    def add_bot(self):

        if self.enter():
            time.sleep(5)
            logger.success(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                           f"бот <fg #898d90>{self.bot_name}</fg #898d90> добавлен")
            self.driver.quit()

    def bot_run(self):

        logger.info(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                       f"запуск бота <fg #898d90>{self.bot_name}</fg #898d90>")
        self.enter()
        # if res:
        result = self.func(self.driver)
        if result:
            logger.success(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                           f"закончил работу")
            return True
        else:
            logger.success(f"<fg #e4abff>{self.session_id} {self.session_name}</fg #e4abff> | "
                           f" НЕ закончил работу")
            return False
