import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser import driver_browser


def test_tvesre(user_, port_, pro=None):
    driver = driver_browser(user_folder=user_, port_=port_, proxy_=pro)
    driver.set_window_size(800, 900)
    driver.get("https://web.telegram.org/k/#?tgaddr=tg%3A//resolve%3Fdomain%3Dtverse%26startapp")
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "popup-button.btn.primary.rp"))
        )
    except:
        pass
    launch_btn = driver.find_elements(By.CLASS_NAME, "popup-button.btn.primary.rp")
    for launch in launch_btn:
        if "LAUNCH" in launch.text:
            launch.click()
            break
    while True:
        print(f"#1 - find 1 class\n"
              f"#2 - find many classes\n"
              f"#3 - click one class\n"
              f"#4 - click many classes\n"
              f"#5 - switch to frame\n"
              f"#6 - switch to default\n"
              f"#7 - if + in\n")
        x = input("insert -> ")
        if x == "1":
            elem = input("enter name class -> ")
            e = driver.find_element(By.CLASS_NAME, elem)
            print("e = ", e)
            print(e.text)
            print("------------------------------------------")
        elif x == "2":
            elem = input("enter name class -> ")
            e = driver.find_elements(By.CLASS_NAME, elem)
            print("len ", len(e))
            for r, el in enumerate(e):
                print(r, el.text)
            print("------------------------------------------")
        elif x == "3":
            elem = input("input class-> ")
            a = driver.find_element(By.CLASS_NAME, elem)
            a.click()
            print("click")
            print("------------------------------------------")
        elif x == "4":
            elem = input("input class and iter-> ")
            c = elem.split(' ')
            time.sleep(2)
            a = driver.find_elements(By.CLASS_NAME, c[0])
            a[int(c[1])].click()
            print("click")
            print("------------------------------------------")
        elif x == "5":
            iframe = driver.find_element(By.TAG_NAME, "iframe")
            print(iframe.get_attribute("src"))
            driver.switch_to.frame(iframe)
            print("switch")
            print("------------------------------------------")
        elif x == "6":
            driver.switch_to.default_content()
            print("switch")
            print("------------------------------------------")
        elif x == "7":
            elements = driver.find_elements(By.CLASS_NAME, "ui-link.blur")
            elements[4].click()
            time.sleep(15)
            elements[3].click()
            time.sleep(2)
            el = driver.find_element(By.CLASS_NAME, "d-flex.align-items-center")
            if "+" in el.text:
                print("+ yes")
            else:
                print("- no")