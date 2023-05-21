from typing import Optional, List, Union
from sqlalchemy.orm import Session
from sqlalchemy.engine import Row
from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql.expression import Select, Insert, Delete
from app.config import Config
from databases import Database

class DatabaseClient:

    def __init__(self, config: Config, tables: Optional[List[str]]):
        self.config = config
        self.engin = create_engine(self.config.host, future=True)
        self.session = Session(bind=self.engin, future=True)

        self.metadata = MetaData()
        self._reflect_metadata()
        if tables:
            self._set_internal_database_tables(tables)
        self.database = Database(self.config.host)

    def _reflect_metadata(self) -> None:
        self.metadata.reflect(bind=self.engin)

    def _set_internal_database_tables(self, tables: List[str]) -> None:
        for table in tables:
            setattr(self, table, self.metadata.tables[table])

    async def get_first(self, query: Select) -> Optional[Row]:
        async with self.database.transaction():
            res = await self.database.fetch_one(query=query)
        return res

    async def get_all(self, query: Select) -> List[Row]:
        async with self.database.transaction():
            res = await self.database.fetch_all(query=query)
        return res

    async def get_paginated(self, query: Select, limit: int, offset: int) -> List[Row]:
        query = query.limit(limit).offset(offset)
        return await self.get_all(query)

    async def execute_in_transaction(self, query: Union[Delete, Insert]):
        async with self.database.transaction():
            await self.database.execute(query)
