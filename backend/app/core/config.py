import os.path
import secrets
import argparse
import click
from typing import Any, Dict, List, Optional, Union
from core import constants
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator, IPvAnyAddress, BaseModel, FilePath


class Settings(BaseSettings):
    PROJECT_NAME: str   # 项目名称 必填
    SECRET_KEY: str = secrets.token_urlsafe(32)   # 登录状态token加密key, 不在配置中固定一个字符会每次运行随机生成一个导致每次重启程序都会登录过期，建议.env中配置一个固定的字符串
    LOGGING_CONFIG_FILE: FilePath = os.path.join(constants.BASE_DIR, 'configs/logging_config.json')   # log格式配置文件路径
    ECHO_SQL: bool = False  # 是否打印sql语句
    AUTO_ADD_PERM_LABEL: bool = False  # 是否在访问到有权限标识的路径的时候自动添加权限标识到数据库

    API_DOMAIN: str = "http://127.0.0.1:9898"  # 本api程序的域名
    WEB_DOMAIN: str = "http://127.0.0.1:8080"  # 前端vue程序的域名

    # 跨域
    BACKEND_CORS_ORIGINS: List[str] = ['*']

    # jwt加密算法
    JWT_ALGORITHM: str = "HS256"

    # FastAPI (Only takes effect in run "python main.py". Don't want to take effect when running with "uvicorn/gunicorn main:app")
    HOST: IPvAnyAddress = "0.0.0.0"     # 允许访问程序的ip， 只允许本地访问使用 127.0.0.1， 只在直接允许程序时候生效
    PORT: int = 9898    # 程序端口，只在直接运行程序的时候生效
    RELOAD: bool = True     # 是否自动重启，只在直接运行程序时候生效

    # sql db
    SQL_USERNAME: str   # 关系型数据库用户名
    SQL_PASSWORD: Optional[str] = None  # 关系型数据库用户密码
    SQL_HOST: Union[AnyHttpUrl, IPvAnyAddress] = "127.0.0.1"    # 关系型数据库HOST地址
    SQL_PORT: int = 3306    # 关系型数据库端口
    SQL_DATABASE: str       # 关系型数据库数据库名
    SQL_TABLE_PREFIX: Optional[str] = 't_'  # 数据库表前缀， 不需要前缀可以置空
    SQLALCHEMY_ENGINE: str = 'mysql+pymysql'   # SQL引擎，修改此处可以快速改变SQL数据库(默认：mysql   可以是其他数据库如 postgresSQL(postgres)  Oracle(oracle+cx_oracle)

    def getSqlalchemyURL(self):
        """
        获取sqlachemy的连接语句， 如SQLite(sqlite))这类数据库可能不一样，请重写。
        """
        user = f"{self.SQL_USERNAME}:{self.SQL_PASSWORD}" if self.SQL_PASSWORD else self.SQL_USERNAME
        return f"{self.SQLALCHEMY_ENGINE}://{user}@{self.SQL_HOST}:{self.SQL_PORT}/{self.SQL_DATABASE}"

    # redis
    REDIS_HOST: str     # Redis Host地址
    REDIS_PASSWORD: Optional[str] = None    # Redis 密码
    REDIS_DB: int = 0   # 选择Redis数据库
    REDIS_PORT: int = 6379  # Redis端口

    def getRedisURL(self):
        """
        获取redis连接语句
        """
        pwd = f':{self.REDIS_PASSWORD}@' if self.REDIS_PASSWORD else ""
        return f"redis://{pwd}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}?encoding=utf-8"

    # email 不填SMTP_HOST代表不使用邮箱服务， 填写后账号注册会有邮件确认
    SMTP_TLS: bool = False
    SMTP_PORT: Optional[int] = 587
    SMTP_HOST: Optional[str] = ""   # SMTP Host地址
    SMTP_USER: Optional[str] = ""   # SMTP用户名
    SMTP_PASSWORD: Optional[str] = ""   # SMTP密码
    EMAIL_FROM_EMAIL: Optional[str] = ""     # 发件人邮箱
    EMAIL_TEMPLATES_DIR: str = "./email-templates/"  # 模板路径


settings = Settings(_env_file=constants.DEFAULT_ENV_FILE, _env_file_encoding='utf-8')
