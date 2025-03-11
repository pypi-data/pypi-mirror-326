from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.orm import sessionmaker
from Exception.ControlledException import DatabaseException
from Utils.Code import DB_SUCCESS
from Utils.Message import DB_STRING_ERROR, DB_CONNECTION_ERROR

class Connection:

    def __init__(self, connection_string: str) -> None:
        if not connection_string:
            raise ValueError(DB_STRING_ERROR)
        
        self.connection_string = connection_string
        self.engine = create_async_engine(self.connection_string, pool_pre_ping=True)
        
        if self.engine is None:
            raise ValueError(DB_CONNECTION_ERROR)
        
        self.session_factory = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_session(self) -> AsyncSession:
        return self.session_factory()

    async def get_raw_conn(self) -> AsyncConnection:
        return await self.engine.connect()

    async def execute_query_return_first_value(self, query: str, params: Dict[str, Any] = None) -> Any:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                return result.scalar()

    async def execute_query_return_data(self, query: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                row = result.fetchone()
                if not row:
                    raise DatabaseException(error=row.message, status_code=row.status_code)

                return dict(zip(result.keys(), row))

    async def execute_query_return_list(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                rows = result.fetchall()
                if not rows:
                    return []
                
                return [dict(zip(result.keys(), row)) for row in rows]

    async def execute_query(self, query: str, params: Dict[str, Any] = None, code: str = DB_SUCCESS) -> str:
        async with (await self.get_session()) as session:
            async with session.begin():
                result = await session.execute(text(query), params)
                row = result.fetchone()
                if row.status_code != code:
                    raise DatabaseException(error=row.message, status_code=row.status_code)
                
                return row.message

    async def execute_query_return_dataset(self, query: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        params = params or {}
        dataset = {}
        async with (await self.get_raw_conn()) as connection:
            async with connection.begin():
                async with connection.begin():
                    result = await connection.execute(query, params)
                    dataset = {}
                    set_index = 1

                    while result.returns_rows:
                        rows = result.fetchall()  # No es necesario `await`, ya que `fetchall()` no es asíncrono
                        if rows:
                            columns_name = result.keys()
                            dataset[f'set_{set_index}'] = [
                                dict(zip(columns_name, row)) for row in rows
                            ]
                            set_index += 1

                        # Mover al siguiente conjunto de resultados
                        result = await result.nextset() 
        return dataset