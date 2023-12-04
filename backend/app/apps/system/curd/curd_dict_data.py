from typing import Tuple

from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.sql import func
from common.curd_base import CRUDBase
from ..models.dictionaries import DictData, DictDetails


class CURDDictData(CRUDBase):

    def getByType(self, db: Session, type: str, status_in: Tuple[int] = None) -> dict:
        status_in = status_in or (0,)
        obj = db.query(self.model).filter(self.model.dict_type == type, self.model.is_deleted == 0,
                                          self.model.status.in_(status_in)).first()  # type: DictData
        if not obj:
            return {}
        dict_details = [{
            'label': detail.dict_label,
            'value': int(detail.dict_value) if detail.dict_value.isdigit() else detail.dict_value,
            'is_default': detail.is_default,
            'remark': detail.remark
        } for detail in obj.dict_detail.filter(DictDetails.is_deleted == 0)]
        return {'type': obj.dict_type, 'name': obj.dict_name, 'details': dict_details}



curd_dict_data = CURDDictData(DictData)