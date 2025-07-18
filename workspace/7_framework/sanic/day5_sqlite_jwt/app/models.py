"""
DB logic for users and notes.
"""
import logging
from app.db import db
from app.auth import hash_password, verify_password

logger = logging.getLogger(__name__)

async def create_user(username, password):
    try:
        hashed_password = hash_password(password)
        await db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        await db.commit()
        logger.info(f"User created: {username}")
    except Exception as e:
        logger.error(f"Error creating user {username}: {e}")
        raise

async def get_user(username):
    try:
        cursor = await db.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        return await cursor.fetchone()
    except Exception as e:
        logger.error(f"Error getting user {username}: {e}")
        raise

async def verify_user_password(username, password):
    try:
        user = await get_user(username)
        if not user:
            logger.warning(f"Login attempt for non-existent user: {username}")
            return None
        if verify_password(password, user[1]):
            logger.info(f"Successful login for user: {username}")
            return user[0]  # Return user ID
        logger.warning(f"Invalid password for user: {username}")
        return None
    except Exception as e:
        logger.error(f"Error verifying password for user {username}: {e}")
        raise

async def add_note(content, user_id):
    try:
        await db.execute("INSERT INTO notes (content, user_id) VALUES (?, ?)", (content, user_id))
        await db.commit()
        logger.info(f"Note added for user {user_id}")
    except Exception as e:
        logger.error(f"Error adding note for user {user_id}: {e}")
        raise

async def get_notes(user_id, limit=5, offset=0):
    try:
        cursor = await db.execute("SELECT id, content FROM notes WHERE user_id = ? LIMIT ? OFFSET ?", (user_id, limit, offset))
        rows = await cursor.fetchall()
        notes = [{"id": r[0], "content": r[1]} for r in rows]
        logger.info(f"Retrieved {len(notes)} notes for user {user_id}")
        return notes
    except Exception as e:
        logger.error(f"Error getting notes for user {user_id}: {e}")
        raise
