"""
Simple async SQLite connection with a single table.
"""
import aiosqlite
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.db = None

    async def connect(self):
        try:
            self.db = await aiosqlite.connect('app.db')
            await self.db.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)')
            await self.db.commit()
            logger.info("Database connected successfully")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    async def disconnect(self):
        if self.db:
            try:
                await self.db.close()
                logger.info("Database disconnected successfully")
            except Exception as e:
                logger.error(f"Error disconnecting from database: {e}")

    async def add_note(self, content):
        if not self.db:
            raise RuntimeError("Database not connected")

        try:
            await self.db.execute('INSERT INTO notes (content) VALUES (?)', (content,))
            await self.db.commit()
            logger.info(f"Note added: {content[:50]}...")
        except Exception as e:
            logger.error(f"Failed to add note: {e}")
            raise

    async def get_notes(self):
        if not self.db:
            raise RuntimeError("Database not connected")

        try:
            cursor = await self.db.execute('SELECT id, content FROM notes')
            notes = await cursor.fetchall()
            await cursor.close()
            return [{"id": row[0], "content": row[1]} for row in notes]
        except Exception as e:
            logger.error(f"Failed to get notes: {e}")
            raise

# Global database instance
db_instance = Database()

# Convenience functions for backward compatibility
async def connect():
    await db_instance.connect()

async def disconnect():
    await db_instance.disconnect()

async def add_note(content):
    await db_instance.add_note(content)

async def get_notes():
    return await db_instance.get_notes()
