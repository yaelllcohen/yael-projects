import sqlite3

# יוצרים או נפתחים למסד נתונים חדש בשם users.db
conn = sqlite3.connect("users.db")

# מצביע לעבודה מול המסד
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")


cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("yael", "1234"))
conn.commit()
