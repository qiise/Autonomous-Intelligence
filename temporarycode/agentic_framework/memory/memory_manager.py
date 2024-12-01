# memory/memory_manager.py
import aiosqlite
from utils.logger import logger

class MemoryManager:
    def __init__(self, db_name="memory.db"):
        self.db_name = db_name
        self.conn = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_name)
        await self.create_table()
        logger.info(f"Connected to memory database '{self.db_name}'.")

    async def create_table(self):
        await self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        await self.conn.commit()
        logger.info("Memory table ensured in database.")

    async def store(self, key, value):
        await self.conn.execute("""
        INSERT INTO memory (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        await self.conn.commit()
        logger.info(f"Stored key '{key}' in memory.")

    async def retrieve(self, key):
        async with self.conn.execute("""
        SELECT value FROM memory WHERE key = ?
        """, (key,)) as cursor:
            row = await cursor.fetchone()
            if row:
                logger.info(f"Retrieved key '{key}' from memory.")
                return row[0]
            else:
                logger.info(f"Key '{key}' not found in memory.")
                return None

    async def close(self):
        await self.conn.close()
        logger.info(f"Closed memory database '{self.db_name}'.")
