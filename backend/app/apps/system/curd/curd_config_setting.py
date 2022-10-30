from sqlalchemy import func
from sqlalchemy.orm import Session

from common.curd_base import CRUDBase
from ..models.config_settings import ConfigSettings


class CURDConfigSetting(CRUDBase):

    def getByKey(self, db: Session, key: str) -> dict:
        obj = db.query(*self.query_columns).filter(self.model.key == key, self.model.is_deleted == 0,
                                                   self.model.status.in_((0,))).first()
        if not obj:
            return {}
        return {'key': obj.key, 'name': obj.name, 'value': int(obj.value) if obj.value.isdigit() else obj.value}


curd_config_setting = CURDConfigSetting(ConfigSettings)