import os.path
import secrets
import argparse
import click
from typing import Any, Dict, List, Optional, Union
from core import constants
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator, IPvAnyAddress, BaseModel, FilePath


class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    LOGGING_CONFIG_FILE: FilePath = os.path.join(constants.BASE_DIR, 'configs/logging_config.json')
    ECHO_SQL: bool = False  # 是否打印sql语句
    AUTO_ADD_PERM_LABEL: bool = False  # 是否在访问到有权限标识的路径的时候自动添加权限标识到数据库

    API_DOMAIN: str = "http://127.0.0.1:9898"
    WEB_DOMAIN: str = "http://127.0.0.1:8080"

    # 跨域
    BACKEND_CORS_ORIGINS: List[str] = ['*']

    # jwt加密算法
    JWT_ALGORITHM: str = "HS256"

    # FastAPI (Only takes effect in run "python main.py". Don't want to take effect when running with "uvicorn/gunicorn main:app")
    HOST: IPvAnyAddress = "0.0.0.0"
    PORT: int = 9898
    RELOAD: bool = True
    DEBUG: bool = True

    # sql db
    SQL_USERNAME: str
    SQL_PASSWORD: Optional[str] = None
    SQL_HOST: Union[AnyHttpUrl, IPvAnyAddress] = "127.0.0.1"
    SQL_PORT: int = 3306
    SQL_DATABASE: str
    SQL_TABLE_PREFIX: Optional[str] = 't_'  # 数据库表前缀， 不需要前缀可以置空
    SQLALCHEMY_ENGINE: str = 'mysql+pymysql'   # SQL引擎，修改此处可以快速改变SQL数据库(默认：mysql   可以是其他数据库如 postgresSQL(postgres)  Oracle(oracle+cx_oracle)  SQLite(sqlite))

    def getSqlalchemyURL(self):
        user = f"{self.SQL_USERNAME}:{self.SQL_PASSWORD}" if self.SQL_PASSWORD else self.SQL_USERNAME
        return f"{self.SQLALCHEMY_ENGINE}://{user}@{self.SQL_HOST}:{self.SQL_PORT}/{self.SQL_DATABASE}?charset=utf8mb4"

    # redis
    REDIS_HOST: str
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_PORT: int = 6379

    def getRedisURL(self):
        pwd = f':{self.REDIS_PASSWORD}@' if self.REDIS_PASSWORD else ""
        return f"redis://{pwd}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}?encoding=utf-8"

    # email
    SMTP_TLS: bool = False
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = ""
    SMTP_USER: Optional[str] = ""
    SMTP_PASSWORD: Optional[str] = ""
    EMAIL_FROM_EMAIL: Optional[str] = ""
    EMAIL_TEMPLATES_DIR: str = "./email-templates/"


settings = Settings(_env_file=constants.DEFAULT_ENV_FILE, _env_file_encoding='utf-8')
