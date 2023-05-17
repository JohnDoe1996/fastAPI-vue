
from redis import Redis
from common.deps import get_db
from core.constants import *
from db.cache import get_redis
from db.session import SessionLocal
from . import app
import traceback
from app.apps.user.curd.curd_user import curd_user
from core.logger import logger


@app.task
def taskPrintDatetime():
    try:
        db = next(get_db())     # type: SessionLocal
        r = get_redis()   # type: Redis
        dt = db.execute("SELECT now();")
        logger.info(dt.fetchall())
        logger.info(f"===== {dt.t} =====")
        users = curd_user.query(db)
        logger.info(users)
        r.incr("taskPrintDatetimeRunCounter")
    except:
        traceback.print_exc()