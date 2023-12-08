from datetime import timedelta
import json
from sqlalchemy import func
from sqlalchemy.orm import Session
try:
    from redis.asyncio import Redis as asyncRedis
except ImportError:
    from aioredis import Redis as asyncRedis
from common.curd_base import CRUDBase
from ..models.config_settings import ConfigSettings


class CURDConfigSetting(CRUDBase):
    CACHE_KEY = "curd_config_setting_KEY_"
    CACHE_ID_KEY = "curd_config_setting_key_ID_"
    EXPIRE_TIME = timedelta(minutes=15)

    def getByKey(self, db: Session, key: str) -> dict:
        obj = db.query(*self.query_columns).filter(self.model.key == key, self.model.is_deleted == 0,
                                                   self.model.status.in_((0,))).first()
        return {} if not obj else {
            'id': obj.id,
            'key': obj.key, 
            'name': obj.name, 
            'value': int(obj.value) if obj.value.isdigit() else obj.value
        }
        
    async def getByKeyWithCache(self, r: asyncRedis, db: Session, key: str) -> dict:
        _key = self.CACHE_KEY + key
        # if res := await r.get(_key):  # python3.8+
        res = await r.get(_key)
        if res:
            return json.loads(res)
        res = self.getByKey(db, key)
        await r.setex(_key, self.EXPIRE_TIME, json.dumps(res))
        await r.setex(self.CACHE_ID_KEY + str(res['id']), self.EXPIRE_TIME, key)
        return res   
    
    async def deleteCacheByID(self, r: asyncRedis, _id: int):
        del_keys = [self.CACHE_ID_KEY + str(_id)]
        # if res := await r.get(_keys[0]):  # python3.8+
        res = await r.get(del_keys[0]) # type: bytes
        if res:
            del_keys.append(self.CACHE_KEY + res.decode('utf-8'))
        await r.delete(*del_keys)
        

curd_config_setting = CURDConfigSetting(ConfigSettings)