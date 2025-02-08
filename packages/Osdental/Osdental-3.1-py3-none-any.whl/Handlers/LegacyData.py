from typing import Dict, Any
from Database.Connection import Connection

class LegacyData:

    def __init__(self, connection_string:str):
        self.db = Connection(connection_string)

    async def get_legacy_data(self) -> Dict[str,Any]:
        return await self.db.execute_query_return_data('EXEC SECURITY.sps_SelectDataLegacy')