from multiprocessing import Pool

from helper import get_active_accounts, get_proxy, logger


if __name__ == '__main__':

    print("1 - pool.map()\n"
          "2 - добавить бота\n"
          "3 - добавить аккаунт\n"
          "4 - запустить один аккаунт\n"
          "5 - запуск по несколько аккаунтов\n"
          "6 - запустить тест\n")

    while True:
        action = int(input("Выбери action -> "))
        if action not in [1, 2, 3, 4, 5, 6]:
            print("Вводи правильно")
        elif action == 1:
            logger.info(f"{len(get_active_accounts())} активных аккаунтов | {len(get_proxy())} прокси")