import os
import time
import random

import psycopg2

from browser import driver_browser
from helper import get_proxy

from dotenv import load_dotenv
load_dotenv('.env')


def add_account():
    number = input("номер телефона -> ")
    conn = psycopg2.connect(dbname=os.getenv('DB_NAME'),
                            host=os.getenv('DB_HOST'),
                            port=os.getenv('DB_PORT'),
                            user=os.getenv('DB_USER'),
                            password=os.getenv('DB_PASSWORD'))
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
                    proxy_=random.choice(get_proxy()),
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
        proxy_=random.choice(get_proxy()),
        dev=False
    )

    driver.get("https://web.telegram.org/k/")
    time.sleep(999999999)


def get_next_accounts(id_=0):
    a_ = int(input("введи id или оставь пустым -> "))
    conn = psycopg2.connect(dbname=os.getenv('DB_NAME'),
                            host=os.getenv('DB_HOST'),
                            port=os.getenv('DB_PORT'),
                            user=os.getenv('DB_USER'),
                            password=os.getenv('DB_PASSWORD'))
    cursor = conn.cursor()
    cursor.execute("SELECT id, number, port FROM data WHERE id = %s ORDER BY id ASC LIMIT 5",
                   (a_ if a_ != "" else id_, ))
    accs = cursor.fetchall()
    return accs