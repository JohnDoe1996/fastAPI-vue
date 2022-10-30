from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
# from db.base_class import Base


engine = create_engine(settings.getSqlalchemyURL(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base.metadata.create_all(engine)
