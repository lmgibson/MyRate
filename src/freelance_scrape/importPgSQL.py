import csv
import psycopg2
from datetime import date

conn = psycopg2.connect("host=localhost dbname=testdb user=Metaverse")
cur = conn.cursor()
today = date.today().strftime("%d%m%Y")
filename = "./data/processed/user_data_" + today + ".csv"
with open(filename) as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        pass
        # call = "INSERT INTO skills VALUES (%s, %s)" % (
        #     row[1], str(row[4]).replace('[', '{').replace(']', '}'))
        # print(call)


def insertUsers():
    conn = psycopg2.connect("host=localhost dbname=testdb user=Metaverse")
    cur = conn.cursor()
    today = date.today().strftime("%d%m%Y")
    filename = "./data/processed/user_data_" + today + ".csv"
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO users VALUES (Default, %s) ON CONFLICT (name) DO NOTHING",
                (row[1],))
    conn.commit()


def insertRates():
    conn = psycopg2.connect("host=localhost dbname=testdb user=Metaverse")
    cur = conn.cursor()
    today = date.today().strftime("%d%m%Y")
    filename = "./data/processed/user_data_" + today + ".csv"
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO rates VALUES (%s, %s, %s) ON CONFLICT (name, scrapeDate) DO NOTHING",
                (row[1:4]))
    conn.commit()


def insertSkills():
    conn = psycopg2.connect("host=localhost dbname=testdb user=Metaverse")
    cur = conn.cursor()
    today = date.today().strftime("%d%m%Y")
    filename = "./data/processed/user_data_" + today + ".csv"
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO skills VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET skillsArray=EXCLUDED.skillsArray",
                (row[1], str(row[4]).replace('[', '{').replace(']', '}')))
    conn.commit()
