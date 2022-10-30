from typing import Union, List
from pydantic import BaseModel, AnyHttpUrl, conint


class ConfigSettingSchema(BaseModel):
    name: str
    key: str
    value: str
    remark: str = ""
    status: int = 0
    order_num: int = 0


class DictDataSchema(BaseModel):
    dict_type: str
    dict_name: str = ""
    remark: str = ""
    status: int = 0
    order_num: int = 0
    
    
class DictDetailSchema(BaseModel):
    dict_label: str
    dict_value: str
    dict_data_id: int
    remark: str = ""
    is_default: bool = False
    status: int = 0
    order_num: int = 0