import sqlite3 as sq

def create_db():
    global base, cur
    base = sq.connect("my_data_base.db")
    cur = base.cursor()
    if base:
        print("[DATABASE] Connected.")
    base.execute("CREATE TABLE IF NOT EXISTS streamers(name TEXT PRIMARY_KEY, viewingTime REAL, airTime TEXT,  \
                 peakViews INTEGER, averageVies INTEGER, subscribers INTEGER)")
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu VALUES (?, ?, ?, ?)", tuple(data.values()))
        base.commit()

async def get_row_by_name(name: str) -> list:
    cur.execute("SELECT name, viewingTime, airTime, peakViews, averageVies, subscribers FROM streamers WHERE name = ?", name)
    return cur.fetchall()

async def get_colums() -> list:
    result = []
    cur.execute("SELECT * from streamers")
    colnames = cur.description
    for row in colnames:
        result.append(row[0])
    return result

