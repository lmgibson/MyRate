import csv
import psycopg2
from datetime import date


def insertUsers():
    conn = psycopg2.connect("host=localhost dbname=testdb user=Metaverse")
    cur = conn.cursor()
    today = date.today().strftime("%d%m%Y")
    filename = "./data/processed/user_data_" + today + ".json"
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO users VALUES (Default, %s) ON CONFLICT DO NOTHING/UPDATE", (row[1],))
    conn.commit()
