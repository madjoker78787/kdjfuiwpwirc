import json
import sys
import zlib
from datetime import datetime
from urllib.parse import urlparse, quote
import subprocess

from loguru import logger

import psycopg2
from psycopg2 import sql

from config import settings


logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)



def start_postgres_process():
    process = subprocess.Popen('sc start "postgresql-X64-17"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()

    if stdout:
        print(stdout.decode())
    if stderr:
        print(stderr.decode())


def generate_telegram_url(link):
    parsed_url = urlparse(link)

    domain = parsed_url.path.split("/")[1]
    appname = parsed_url.path.split("/")[2] if len(parsed_url.path.split("/")) > 2 else None

    op = f"tg://resolve?domain={domain}"

    if appname:
        op += f"&appname={appname}"

    query_params = parsed_url.query
    if query_params:
        op += f"&{query_params}"

    final_url = f"https://web.telegram.org/k/#?tgaddr={quote(op)}"

    return final_url
# https://web.telegram.org/k/#?tgaddr=tg%3A%2F%2Fresolve%3Fdomain%3Dnotpixel%26appname%3Dapp%26startapp
# print(generate_telegram_url("https://t.me/tverse?startapp"))

def decode_string(s: bytes):
    decompressed = zlib.decompress(s, zlib.MAX_WBITS | 16)
    d_string = decompressed.decode('utf-8')
    decode_json = json.loads(d_string)
    return decode_json


def get_proxy():
    list_proxy = []
    with open('proxy.txt', 'r') as file:
        for item in file:
            list_proxy.append(item)
    return list_proxy


def init_postgres():
    conn = psycopg2.connect(
        dbname="postgres",
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [settings.DB_NAME])
    exists = cursor.fetchone() is not None
    if not exists:
        logger.info("создаем базу данных Telegram")
        query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier("Telegram"))
        cursor.execute(query)
        logger.info("база данных Telegram успешно создана")
        cursor.close()
        conn.close()
    else:
        logger.info("база данных Telegram уже создана")

    if not check_table_exist(table_name=settings.TABLE_TELEGRAM):
        conn = psycopg2.connect(
            dbname=settings.DB_NAME,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursor = conn.cursor()
        logger.info(f"создаем таблицу {settings.TABLE_TELEGRAM}")
        query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    number VARCHAR(100),
                    port VARCHAR(100),
                    work VARCHAR(100) DEFAULT 1
                )
                """).format(sql.Identifier(settings.TABLE_TELEGRAM))
        cursor.execute(query)
        conn.commit()
        cursor.execute("INSERT INTO data(number, port, work) VALUES(%s, %s, %s)", ("test", "8742", "0"))
        conn.commit()
        cursor.close()
        conn.close()
        logger.success("таблица data создана")
    else:
        logger.info("таблица data уже создана")

def check_table_exist(table_name):
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    query = """
    SELECT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_name = %s
    );
    """
    cursor.execute(query, (table_name,))
    table_exists = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if table_exists:
        return True
    else:
        return False


def create_table(table_name):
    if not check_table_exist(table_name):
        conn = psycopg2.connect(
            dbname=settings.DB_NAME,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursor = conn.cursor()
        conn.autocommit = True
        logger.info(f"создаем таблицу {settings.DB_NAME}.{table_name}")
        query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    data_id VARCHAR(100),
                    last_visit VARCHAR(100)
                )
                """).format(sql.Identifier(table_name))
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        logger.success(f"таблица {table_name} создана")


def get_active_accounts():
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, number, port FROM data WHERE work = %s", ("1", ))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def get_last_visit(id_, table_name):
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()

    query = sql.SQL("SELECT last_visit FROM {} WHERE data_id = %s").format(sql.Identifier(table_name))
    cursor.execute(query, (str(id_),))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result if result is not None else ["01.01.1970 00:00"]


def update_time(id_, table_name):
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()

    query = sql.SQL("UPDATE {} SET last_visit = %s WHERE data_id = %s").format(sql.Identifier(table_name))
    cursor.execute(query, (datetime.now().strftime("%d.%m.%Y %H:%M"), str(id_),))
    conn.commit()
    cursor.close()
    conn.close()