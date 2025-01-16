
from multiprocessing import Pool

from start_methods import add_account, start_one

from proxy_list import lst

from BotClass import Bots
from helper import (get_active_accounts,
                    logger,
                    init_postgres,
                    check_table_exist,
                    create_table)

from tests import test_tvesre

from config import settings

if __name__ == '__main__':

    print("1 - pool.map()\n"
          "2 - добавить бота(рефералы)\n"
          "3 - добавить аккаунт\n"
          "4 - запустить один аккаунт\n"
          "5 - запуск по несколько аккаунтов\n"
          "6 - запустить тест\n"
          "7 - инициализация базы данных и таблиц\n"
          "8 - добавить таблицу\n")

    while True:
        try:
            action = int(input("Выбери action -> "))
            if action not in [1, 2, 3, 4, 5, 6, 7, 8]:
                print("Вводи правильно")
            elif action == 1:
                logger.info(f"{len(get_active_accounts())} активных аккаунтов | {len(lst)} прокси")
                with Pool(processes=settings.WORKERS) as pool:
                    # pool.map(check_bots, get_active_accounts())
                    pool.map(Bots().bot_run, get_active_accounts())
            elif action == 2:
                while True:
                    table = input("добавить бота в новую таблицу? [ y/n ]")
                    if table.lower() not in ['y', 'n']:
                        print("не правильный выбор, еще раз")
                    elif table.lower() == 'y':
                        table_name = input("введи название новой таблицы(например название бота) -> ")
                        if not check_table_exist(table_name=table_name):
                            create_table(table_name=table_name)
                    elif table.lower() == 'n':
                        pass
                    bot_ulr = input("введи url бота -> ")
                    dev = input("запуск с devtools? [ y/n ]")
                    d = False
                    if dev.lower() == 'y':
                        d = True
                    with Pool(processes=settings.WORKERS) as pool:
                        pool.map(Bots(url=bot_ulr, dev=d).add_bot, get_active_accounts())
                        break
            elif action == 3:
                add_account()
            elif action == 4:
                start_one()
                break
            elif action == 5:
                ...
            elif action == 6:
                test_tvesre(user_="test", port_="8742")
            elif action == 7:
                try:
                    init_postgres()
                except Exception as e:
                    print(e)
            elif action == 8:
                table_name = input("введи название новой таблицы(например название бота) -> ")
                create_table(table_name=table_name)
        except KeyboardInterrupt:
            print("остановлен")
