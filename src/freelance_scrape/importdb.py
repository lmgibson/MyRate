import csv
import psycopg2
import os
from datetime import date


def insertUsers(filename):
    """
    Inserts user names into a table named "users":
      1. id SERIAL PRIMARY KEY
      2. name VARCHAR (120) NOT NULL
    """
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


def insertRates(filename):
    """
    Inserts rates data into a table named "rates" that is formatted:
      1. name VARCHAR (120) NOT NULL
      2. scrapeDate date NOT NULL
      3. rate float
      PRIMARY KEY (name, scrapeDate)
    """
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


def insertSkills(filename):
    """
    Inserts data into a table named "skills" that is of the following format:
      1. name VARCHAR (120) PRIMARY KEY
      2. skillsArray text[][]
    """
    conn = psycopg2.connect("host=localhost dbname=testdb user=Metaverse")
    cur = conn.cursor()
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute(
                "INSERT INTO skills VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET skillsArray=EXCLUDED.skillsArray",
                (row[1], str(row[4]).replace('[', '{').replace(']', '}')))
    conn.commit()


# today = date.today().strftime("%d%m%Y")
# filename = "./data/processed/user_data_" + today + ".csv"
# os.remove(filename)
