import os
import asyncache
import aiosqlite

from control_db.user import UserDB
from control_db.premium_user import PremiumUser
from control_db.premium_operations import PremiumOperations

class Database(UserDB, PremiumOperations, PremiumUser):
    @classmethod
    @asyncache.cached({})
    async def setup(cls):
        if not os.path.exists("./data"):
            os.mkdir("./data")

        base = await aiosqlite.connect("data/database.db")
        cur = await base.cursor()
        
        if base:
            print("DATA BASE CONNECTED")

        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS user(
                telegram_id       INTEGER NOT NULL, 
                first_name        TEXT,     -- ім`я
                username          TEXT,     -- особливе ім`я
                date_join         TEXT     -- дата коли перший раз написав боту
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS premium_user(
                telegram_id       INTEGER NOT NULL, 
                is_premium        BOOLEAN,  -- чи активна зараз підписка
                bought_premium    INTEGER,    -- к-ть купівель підписки 
                date_purchase     TEXT     -- коли купив підписку яка зараз активна
            )
            """
        )
        await base.execute(
            """
            CREATE TABLE IF NOT EXISTS premium_operations(
                telegram_id       INTEGER NOT NULL, 
                data_operation    TEXT,
                price             INTEGER
            )
            """
        )
        
        await base.commit()
        return cls(base, cur)