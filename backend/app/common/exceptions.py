import json
import traceback
from typing import Optional, Dict, Any
from core.logger import logger
from fastapi import FastAPI, status, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from .error_code import *
from core.config import settings
from .resp import respErrorJson
from starlette.requests import Request


def customExceptions(app: FastAPI):
    # 重写HTTPException为项目中需要的返回类型
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handle(request: Request, exc: StarletteHTTPException):
        err = exc.err if hasattr(exc, 'err') else ErrorBase(code=exc.status_code)
        return respErrorJson(error=err, status_code=exc.status_code, msg=exc.detail)

    # 重写RequestValidationError为项目中需要的返回类型
    @app.exception_handler(RequestValidationError)
    async def http_exception_handle(request: Request, exc: RequestValidationError):
        err = ERROR_PARAMETER_ERROR
        return respErrorJson(error=err, status_code=err.code, data={'errors': json.loads(exc.json())})
    
    # 重写所有错误返回项目需要的格式错误 需要的时候可以用作错误消息推送
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        # 处理未被捕获的其他异常
        err = ERROR_INTERNAL
        err_msg = traceback.format_exc()
        data = {'error_type': str(type(exc)), 'error_msg': str(exc),'error_detail': err_msg} 
        # # 使用MongoDB存放错误记录
        # mongo = app.mongo # type: pymongo.database.Database
        # if mongo:
        #     mongo['request_exceptions'].insert_one(data)
        return respErrorJson(error=err, status_code=err.code, data=data if settings.DEBUG else {})


class CustomErrorBase(HTTPException):
    err: ErrorBase

    def __init__(self, headers: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=status.HTTP_200_OK,
                         detail=self.err.msg,
                         headers=headers)


class UserTokenError(CustomErrorBase):
    err = ERROR_USER_TOKEN_FAILURE


class UserPermError(CustomErrorBase):
    err = ERROR_USER_PREM_ERROR
