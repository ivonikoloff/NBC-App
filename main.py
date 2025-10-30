import sqlite3, datetime, os

DB = 'nbc.db'

def init_db():
    fresh = not os.path.exists(DB)
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        egn TEXT,
        status TEXT,
        joined_at TEXT,
        left_at TEXT,
        notes TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER,
        amount REAL,
        date TEXT,
        method TEXT,
        doc_no TEXT,
        note TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        budget REAL,
        owner TEXT,
        status TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        due_date TEXT,
        channel TEXT,
        status TEXT
    )
    """)

    if fresh:
        today = datetime.date.today().isoformat()
        c.executemany(
            "INSERT INTO members(name, egn, status, joined_at, notes) VALUES (?,?,?,?,?)",
            [
                ("Калоян Йорданов Колев", "0000000000", "Редовен", today, "Председател на УС"),
                ("Марианна Светлозарова Александрова", "0000000001", "Редовен", today, "УС"),
                ("Цветан Огнянов Вълков", "0000000002", "Почетен", today, "Консултант"),
            ]
        )

        c.executemany(
            "INSERT INTO payments(member_id, amount, date, method, doc_no, note) VALUES (?,?,?,?,?,?)",
            [
                (1, 50.00, today, "Банков превод", "RV-1", "Членски внос"),
                (2, 50.00, today, "В брой", "RV-2", "Членски внос"),
            ]
        )

        c.execute(
            "INSERT INTO projects(name, budget, owner, status) VALUES (?,?,?,?)",
            ("Кулинарен фестивал 2025", 1500.00, "УС", "Активен")
        )

        c.executemany(
            "INSERT INTO reminders(title, due_date, channel, status) VALUES (?,?,?,?)",
            [
                ("Декларация към НАП", "2025-03-31", "email", "очаква"),
                ("Отчет към НСИ", "2025-04-01", "email", "очаква"),
                ("Публикуване ГФО в ТР", "2025-06-30", "email", "очаква"),
            ]
        )

    conn.commit()
    conn.close()
