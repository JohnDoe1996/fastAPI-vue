import json
from typing import Optional, Dict, Any
from core.logger import logger
from fastapi import FastAPI, status, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from .error_code import ErrorBase, ERROR_USER_TOKEN_FAILURE, ERROR_PARAMETER_ERROR, ERROR_NOT_FOUND, \
    ERROR_USER_PREM_ERROR
from .resp import respErrorJson
from starlette.requests import Request


def customExceptions(app: FastAPI):
    # 重写HTTPException为项目中需要的返回类型
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handle(request: Request, exec: StarletteHTTPException):
        err = exec.err if hasattr(exec, 'err') else ErrorBase(code=exec.status_code)
        return respErrorJson(error=err, status_code=exec.status_code, msg=exec.detail)

    # 重写RequestValidationError为项目中需要的返回类型
    @app.exception_handler(RequestValidationError)
    async def http_exception_handle(request: Request, exec: RequestValidationError):
        err = ERROR_PARAMETER_ERROR
        return respErrorJson(error=err, status_code=err.code, data={'errors': json.loads(exec.json())})


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
