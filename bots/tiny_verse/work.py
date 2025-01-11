import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def tiny_verse_func(driver):
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-link.blur"))
        )
    except:
        pass
    elements = driver.find_elements(By.CLASS_NAME, "ui-link.blur")
    elements[4].click()
    time.sleep(15)
    elements[3].click()
    time.sleep(2)
    el = driver.find_element(By.CLASS_NAME, "d-flex.align-items-center")
    if "+" not in el.text:
        driver.find_element(By.CLASS_NAME, "ui-button").click()
        time.sleep(5)
    # print("записываем дату в базу")
    return True