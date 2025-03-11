from typing import Dict, Any
from Database.Connection import Connection

class CatalogData:

    def __init__(self, connection_string:str):
        self.db = Connection(connection_string)
    
    async def get_data(self, catalog_name:str) -> Dict[str,Any]:
        query = """EXEC CATALOG.sps_GetCatalogByName @i_nameCatalog = :catalog_name"""
        rows = await self.db.execute_query_return_list(query, {'catalog_name': catalog_name})
        return {
            row.name: row.value for row in rows if row.value
        }