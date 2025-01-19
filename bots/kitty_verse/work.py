import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver


def kitty_verse_func(driver: webdriver.Chrome):
    print("имитация работы kitty")
    time.sleep(30)
    return True