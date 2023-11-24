from typing import Any, Iterable

import aiosqlite

from promobot_appeal_processing import Prediction

from misc.data_models import DatabaseRow
from misc.config import Paths


class Database:
    def __init__(self) -> None:
        self.connection: aiosqlite.Connection | None = None


    async def create(self) -> None:
        connection = await aiosqlite.connect(Paths.database)

        await connection.execute(
            "CREATE TABLE IF NOT EXISTS "
            "appeals (text text, topic text, topic_group text, executor text, "
            "is_processed bool NOT NULL DEFAULT 0 CHECK (is_processed IN (0, 1)))"
        )
        await connection.commit()

        self.connection = connection

    async def close(self) -> None:
        await self.connection.close()


    async def fetchall(
        self,
        sql: str,
        parameters: Iterable[Any] | None = None
    ) -> tuple[DatabaseRow]:
        """
        Executes the given SQL query and returns the result

        :param sql: SQL query to execute
        :param parameters: Parameters for the SQL query
        :return: Results as a tuple
        """
        model_columns = DatabaseRow.model_fields.keys()

        cursor: aiosqlite.Cursor = await self.connection.execute(sql, parameters)
        result = tuple(map(lambda row: DatabaseRow(**dict(zip(model_columns, row))), await cursor.fetchall()))
        await cursor.close()

        return result

    async def commit(self) -> None:
        await self.connection.commit()

    async def execute_and_commit(self, sql: str, parameters: Iterable[Any] | None = None) -> None:
        """
        Executes the given SQL query with changes to the database and commits them

        :param sql: SQL statement to execute
        :param parameters: Parameters to the sql statement
        :return: None
        """
        await self.connection.execute(sql, parameters)
        await self.connection.commit()


    async def insert_appeal(self, text: str, prediction: Prediction) -> None:
        await self.connection.execute(
            "INSERT INTO appeals (text, topic, topic_group, executor) VALUES (?, ?, ?, ?)",
            (text, prediction.topic, prediction.topic_group, prediction.executor)
        )

    async def fetch_non_processed_appeals(self) -> tuple[DatabaseRow]:
        return await self.fetchall("SELECT rowid, * FROM appeals WHERE is_processed = 0")

    async def mark_processed(self, id: int) -> None:
        await self.execute_and_commit(
            "UPDATE appeals SET is_processed = 1 WHERE id = ?", (id,)
        )


database = Database()
