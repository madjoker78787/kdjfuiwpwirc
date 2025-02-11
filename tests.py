import os
import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.devtools import

from browser import driver_browser


def test_main(user_, port_, pro=None):
    driver = driver_browser(user_folder=user_, port_=port_, proxy_=pro, dev=False)
    driver.set_window_size(800, 900)
    driver.get("https://web.telegram.org/k/")
    # driver.get("https://web.telegram.org/k/#?tgaddr=tg%3A//resolve%3Fdomain%3Dtverse%26startapp")
    # try:
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "popup-button.btn.primary.rp"))
    #     )
    # except:
    #     pass
    # launch_btn = driver.find_elements(By.CLASS_NAME, "popup-button.btn.primary.rp")
    # for launch in launch_btn:
    #     if "LAUNCH" in launch.text:
    #         launch.click()
    #         break
    while True:
        print(f"#1 - find 1 class\n"
              f"#2 - find many classes\n"
              f"#3 - click one class\n"
              f"#4 - click many classes\n"
              f"#5 - switch to frame\n"
              f"#6 - switch to default\n"
              f"#7 - if + in\n"
              f"#8 - my FUNC\n"
              f"#9 - click one css element\n"
              f"#10 - click many css elements\n")
        x = input("insert -> ")
        try:
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
            elif x == "8":
                # t = input("element -> ")
                target_element = driver.find_element(By.CLASS_NAME,
                                                     'homeFooter')  # Замените на селектор вашего элемента
                print(target_element)
                # Получение координат элемента
                location = target_element.location
                size = target_element.size
                # x_center = location['x'] + size['width'] // 2
                x_center = 172
                # y_center = location['y'] + size['height'] // 2
                y_center = 305
                driver.execute_script("""
                    const targetElement = document.querySelector('.homeFooter')
                    if (targetElement) {
                        const touchStartEvent = new TouchEvent('touchstart', {
                                bubbles: true,
                                cancelable: true,
                                touches: [{ clientX: 0, clientY: 0 }],
                                targetTouches: [],
                            });
                            targetElement.dispatchEvent(touchStartEvent);
                    } else {
                        console.error('Элемент не найден');
                    }
                """)
            elif x == "9":
                el = input("enter tag element -> ")
            elif x == "10":
                el = input("enter tag element and iter (img, 105) -> ")
                els = el.split(', ')
                a = driver.find_elements(By.TAG_NAME, els[0])
                a[int(els[1])].click()

        except Exception as e:
            print(e)