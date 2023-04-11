import sqlite3 as sq
from datetime import datetime

def create_db():
    global base, cur
    base = sq.connect("my_data_base.db")
    cur = base.cursor()
    if base:
        print("[DATABASE] Connected.")
    base.execute("CREATE TABLE IF NOT EXISTS streamers(name TEXT PRIMARY_KEY, viewingTime REAL, airTime TEXT,  \
                 peakViews INTEGER, averageVies INTEGER, subscribers INTEGER, FOREIGN KEY (file_id)  REFERENCES files (id))")
    base.commit()
    base.execute("CREATE TABLE IF NOT EXISTS files(id INTEGER PRIMARY_KEY AUTOINCREMENT, name TEXT, date_time TEXT)")
    base.commit()

async def get_row_by_name(name: str) -> list:
    cur.execute("SELECT name, viewingTime, airTime, peakViews, averageVies, subscribers FROM streamers WHERE name = ?", name)
    return cur.fetchall()

async def add_file(name: str) -> None:
    cur.execute("INSERT INTO files VALUES (?, ?)", (name, datetime.now().strftime("%Y-%M-%D %I:%M%p")))
    base.commit()

async def get_colums() -> list:
    result = []
    cur.execute("SELECT * from streamers")
    colnames = cur.description
    for row in colnames:
        result.append(row[0])
    return result

