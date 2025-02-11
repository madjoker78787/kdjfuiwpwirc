import psycopg2

def dump_data_db():
    conn1 = psycopg2.connect(dbname="Telegram", host="localhost", user="postgres", password="postgres", port="5432")
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT number, port, seed FROM data WHERE work IN (%s) ORDER BY id ASC", (1,))
    a = cursor1.fetchall()
    cursor1.close()
    conn1.close()

    d = "\ndb = [\n"
    for x in a:
        d += f"    [\"{str(x[0]).replace(' ', '-')}\", \"{x[1]}\", "
        d += "\"" + str(x[2]).replace('\n', ' ') + "\"], \n"
    d += "]"

    with open("data.py", "w") as file:
        file.write(d)
