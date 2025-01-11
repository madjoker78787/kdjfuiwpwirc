import os
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv

from THIS_IS_NEW.bots.tiny_verse.config import settings

load_dotenv("../../.env")

def check_time(id_):
    conn = psycopg2.connect(db_name=os.getenv('DB_NAME'),
                            host=os.getenv('DB_HOST'),
                            port=os.getenv('DB_PORT'),
                            user=os.getenv('DB_USER'),
                            password=os.getenv('DB_PASSWORD'))
    cursor = conn.cursor()
    cursor.execute("SELECT last_visit FROM tiny_verse WHERE id = %s", (id_, ))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    last_visit = datetime.strptime(data[0], "%d.%m.%Y %H:%M")
    if last_visit + timedelta(minutes=settings.DELAY) < datetime.now():
        return True
    else:
        return False

def update_time(id_):
    conn = psycopg2.connect(db_name=os.getenv('DB_NAME'),
                            host=os.getenv('DB_HOST'),
                            port=os.getenv('DB_PORT'),
                            user=os.getenv('DB_USER'),
                            password=os.getenv('DB_PASSWORD'))
    cursor = conn.cursor()
    cursor.execute("UPDATE tiny_verse SET last_visit = %s WHERE id = %s", (
        datetime.now().strftime("%d.%m.%Y %H:%M"), id_,
    ))
    conn.commit()
    cursor.close()
    conn.close()