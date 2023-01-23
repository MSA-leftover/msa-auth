import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from ..settings import get_settings, ProjectSettings

settings: ProjectSettings = get_settings()


def get_uri():
    return f"{settings.db.protocol}+{settings.db.protocol}db://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}"


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as exception:
        logging.exception(exception)
        db.rollback()
    finally:
        logging.info("db closed")
        db.close()


engine = create_engine(get_uri(), encoding="utf-8")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
