"""
Initialize SQLite database and create tables
"""
import aiosqlite

db = None

async def connect():
    global db
    db = await aiosqlite.connect("app.db")
    await db.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    await db.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        content TEXT,
        user_id INTEGER
    )
    """)
    await db.commit()

async def disconnect():
    global db
    if db is not None:
        await db.close()
