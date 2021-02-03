import csv
import psycopg2


def insertUsers(data):
    conn = psycopg2.connect("host=localhost dbname=testdb user=Metaverse")
    cur = conn.cursor()
    with open("./data/processed/user_data_01112020.csv") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO users VALUES (Default, %s)", (row[1],))
    conn.commit()
