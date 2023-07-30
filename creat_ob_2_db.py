import sqlite3 as sq


def createNewBase():
    with sq.connect('yamen_ob_2.db') as con:
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Screen (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        usable INTEGER NOT NULL DEFAULT 1,
        readed INTEGER NOT NULL DEFAULT 0,
        errors_log TEXT,
        strline TEXT
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Fields (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        time TEXT,
        date_time TEXT,
        activ INTEGER,
        rait REAL,
        grate INTEGER,
        all_profit REAL,
        cash_profit REAL,
        card_profit REAL,
        orders INTEGER,
        commission INTEGER,
        balance REAL,
        tips REAL,
        name TEXT NOT NULL,
        verified INTEGER NOT NULL DEFAULT 0
        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS Truedate (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        day INTEGER,
        month INTEGER,
        year INTEGER,
        activ INTEGER,
        rait REAL,
        grate INTEGER,
        all_profit REAL,
        cash_profit REAL,
        card_profit REAL,
        orders INTEGER,
        commission INTEGER,
        balance REAL,
        tips REAL

        )""")

    # print('Новая база созданна')


if __name__ == '__main__':
    createNewBase()
