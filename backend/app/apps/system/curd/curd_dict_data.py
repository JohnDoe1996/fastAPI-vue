from datetime import timedelta
import json
from typing import Tuple
try:
    from redis.asyncio import Redis as asyncRedis
except ImportError:
    from aioredis import Redis as asyncRedis
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.sql import func
from common.curd_base import CRUDBase
from ..models.dictionaries import DictData, DictDetails


class CURDDictData(CRUDBase):
    CACHE_KEY = "curd_dict_data_TYPE_"
    CACHE_ID_KEY = "curd_dict_data_type_ID_"
    EXPIRE_TIME = timedelta(minutes=15)
    
    def getByType(self, db: Session, _type: str, status_in: Tuple[int] = None) -> dict:
        status_in = status_in or (0,)
        obj = db.query(self.model).filter(self.model.dict_type == _type, self.model.is_deleted == 0,
                                          self.model.status.in_(status_in)).first()  # type: DictData
        if not obj:
            return {}
        dict_details = [{
            'id': detail.id,
            'label': detail.dict_label,
            'value': int(detail.dict_value) if detail.dict_value.isdigit() else detail.dict_value,
            'is_default': detail.is_default,
            'remark': detail.remark
        } for detail in obj.dict_detail.filter(DictDetails.is_deleted == 0)]
        return {'id': obj.id, 'type': obj.dict_type, 'name': obj.dict_name, 'details': dict_details}

    async def getByTypeWithCache(self, r: asyncRedis, db: Session, _type: str) -> dict:
        _key = self.CACHE_KEY + _type
        # if res := await r.get(_key):  # python3.8+
        res = await r.get(_key)
        if res:
            return json.loads(res)
        res = self.getByType(db, _type)
        await r.setex(_key, self.EXPIRE_TIME, json.dumps(res))
        await r.setex(self.CACHE_ID_KEY + str(res['id']), self.EXPIRE_TIME, _type)
        return res
        
    async def deleteCacheByID(self, r: asyncRedis, _id: int):
        del_keys = [self.CACHE_ID_KEY + str(_id)]
        # if res := await r.get(_keys[0]):    # python3.8+
        res = await r.get(del_keys[0]) # type: bytes
        if res:
            del_keys.append(self.CACHE_KEY + res.decode('utf-8'))
        await r.delete(*del_keys)

curd_dict_data = CURDDictData(DictData)