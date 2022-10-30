from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apps import api_router
from starlette.middleware.cors import CORSMiddleware

from common.exceptions import customExceptions
from core.config import settings
from db.cache import registerRedis


def createApp():
    app = FastAPI(title=settings.PROJECT_NAME)
    # set middleware
    # register_middleware(app)
    # api router
    app.include_router(api_router, prefix="/api/v1")
    # set socketio
    # app.mount('/', socket_app)
    # set static files
    app.mount("/media", StaticFiles(directory="media"), name="media")   # 媒体文件
    # allow cross domain
    app.add_middleware(CORSMiddleware, allow_origins=settings.BACKEND_CORS_ORIGINS,
                       allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    # set redis
    registerRedis(app)
    # set custom exceptions
    customExceptions(app)
    # # print all path
    # for _route in app.routes:
    #     r = _route.__dict__
    #     print(r['path'], r.get('methods', {}))
    return app



app = createApp()


if __name__ == '__main__':
    import uvicorn
    # Don't set debug/reload equals True in release, because TimedRotatingFileHandler can't support multi-prcoess
    # please used "uvicorn --host 127.0.0.1 --port 8000 main:app --env-file ./configs/.env" run in release, and used "python main.py" in dev
    uvicorn.run(
        app='main:app',
        host=str(settings.HOST),
        port=settings.PORT,
        debug=settings.DEBUG,
        reload=settings.RELOAD,
        log_config=str(settings.LOGGING_CONFIG_FILE)
    )