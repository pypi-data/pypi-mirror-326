from uuid import UUID
from Database.Connection import Connection
from RedisCache.Redis import RedisCacheAsync
from Exception.ControlledException import UnauthorizedException
from Utils.Message import UNAUTHORIZATED
from Utils.Code import DB_UNAUTHORIZATED
from Utils.Constant import CHARSET

class TokenValidate:

    def __init__(self, connection_string:str):
        self.db = Connection(connection_string)
        self.redis = RedisCacheAsync()

    async def validate(self, token_id:UUID, user_id:UUID) -> bool:
        query = """ 
        EXEC SECURITY.sps_ValidateUserToken  
        @i_idToken = :token_id,
        @i_idUser = :user_id
        """
        await self.redis.connect()
        redis_response = await self.redis.exists(token_id)
        if redis_response:
            data_byte = await self.redis.get_str(token_id)
            return data_byte.decode(CHARSET)
        
        is_auth = await self.db.execute_query_return_first_value(query, {'token_id': token_id, 'user_id': user_id})
        if not is_auth:
            raise UnauthorizedException(error=UNAUTHORIZATED, status_code=DB_UNAUTHORIZATED)
            
        await self.redis.set_str(token_id, is_auth, ttl=1800)
        await self.redis.close()
        return is_auth

