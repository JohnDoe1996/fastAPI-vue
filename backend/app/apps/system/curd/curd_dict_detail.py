from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from common.curd_base import CRUDBase
from ..models.dictionaries import DictDetails


class CURDDictDetail(CRUDBase):
    def get_max_order_num(self, db: Session, *, dict_data_id: int ) -> int:
        res = db.query(func.max(DictDetails.order_num).label('max_order_num')).filter(
            DictDetails.dict_data_id == dict_data_id, DictDetails.is_deleted == 0
        ).first()
        return res['max_order_num'] or 0


curd_dict_detail = CURDDictDetail(DictDetails)