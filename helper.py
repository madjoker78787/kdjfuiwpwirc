import json
import os
import sys
import zlib
from datetime import datetime
from urllib.parse import urlparse, quote

from loguru import logger

import psycopg2
from psycopg2 import sql

from dotenv import load_dotenv

logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

load_dotenv('.env')


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


def get_active_accounts():
    conn = psycopg2.connect(db_name=os.getenv('DB_NAME'),
                            host=os.getenv('DB_HOST'),
                            port=os.getenv('DB_PORT'),
                            user=os.getenv('DB_USER'),
                            password=os.getenv('DB_PASSWORD'))
    cursor = conn.cursor()
    cursor.execute("SELECT id, number, port FROM data WHERE work = %s", ("1", ))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def get_data(id_, table_name):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_MAIN_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = conn.cursor()

    cursor.execute("SELECT number, port FROM data WHERE id = %s", (id, ))

    r1 = cursor.fetchone()

    query = sql.SQL("SELECT last_visit FROM {} WHERE data_id = %s").format(sql.Identifier(table_name))
    cursor.execute(query, (id_,))
    r2 = cursor.fetchone()

    cursor.close()
    conn.close()

    result = [
        id_, #id 0
        r1[0], #number 1
        r1[1], #port 2
        r2[0] #last_visit 3
    ]

    return result


def update_time(id_, table_name):
    conn = psycopg2.connect(db_name=os.getenv('DB_NAME'),
                            host=os.getenv('DB_HOST'),
                            port=os.getenv('DB_PORT'),
                            user=os.getenv('DB_USER'),
                            password=os.getenv('DB_PASSWORD'))
    cursor = conn.cursor()

    query = sql.SQL("UPDATE {} SET last_visit = %s WHERE data_id = %s").format(sql.Identifier(table_name))
    cursor.execute(query, (datetime.now().strftime("%d.%m.%Y %H:%M"), id_,))
    conn.commit()
    cursor.close()
    conn.close()