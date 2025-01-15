
import time
import random

import psycopg2

from browser import driver_browser
from proxy_list import lst

from config import settings

def start_one():
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, number FROM data ORDER BY id")
    nums = cursor.fetchall()
    for i in nums:
        print(f"id [ {i[0]} ] номер [ {i[1]} ]")

    id_ = int(input("выбери номер(не id) -> "))
    cursor.execute("SELECT id, number, port FROM data WHERE id = %s", (id_, ))
    num = cursor.fetchone()
    driver = driver_browser(user_folder=num[1],
                            port_=num[2],
                            # proxy_=random.choice(lst)
                            )
    cursor.close()
    conn.close()
    driver.set_window_size(950, 1000)
    driver.get("https://web.telegram.org/k/")

    try:
        time.sleep(999999999)
    except KeyboardInterrupt:
        print("остановлен")


def add_account():
    number = input("номер телефона -> ")
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT number, port FROM data")
    numbers = cursor.fetchall()
    for i in numbers:
        if number.replace(' ', '') == str(i[0]).replace(' ', ''):
            res = input(f"Номер {str(i[0]).replace('-', '')} уже есть, обновить? [ y/n ] ")
            if res.lower() == "y":
                print("Обновление...")
                driver = driver_browser(
                    user_folder=number,
                    port_=8742,
                    # proxy_=random.choice(lst),
                    dev=False
                                        )
                driver.get("https://web.telegram.org/k/")
                time.sleep(999999999)

    not_exist = input("Номера нет, продолжить? [Y/N] ")
    if not_exist.lower() == "n":
        return
    print("Продолжаем...")
    cursor.execute("SELECT port FROM data ORDER BY id DESC LIMIT 1")
    port = cursor.fetchone()
    cursor.execute("INSERT INTO data(number, port) VALUES(%s, %s)",
                   (number, int(port[0]) + 1, ))
    conn.commit()
    cursor.close()
    conn.close()

    driver = driver_browser(
        user_folder=number,
        port_=int(port[0]) + 1,
        proxy_=random.choice(lst),
        dev=False
    )

    driver.get("https://web.telegram.org/k/")
    try:
        time.sleep(999999999)
    except KeyboardInterrupt:
        print("остановлен")


def get_next_accounts(id_=0):
    a_ = int(input("введи id или оставь пустым -> "))
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, number, port FROM data WHERE id = %s ORDER BY id ASC LIMIT 5",
                   (a_ if a_ != "" else id_, ))
    accs = cursor.fetchall()
    return accs