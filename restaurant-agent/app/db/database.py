from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# echo=False in normal use; flip to True locally if you need to see raw SQL.
engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,  # recycles dead connections instead of failing on them
    fast_executemany=True,  # speeds up bulk inserts with pyodbc
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a DB session and always closes it,
    even if the request raises. Use like:

        from fastapi import Depends
        from app.db.database import get_db

        @router.get("/menu")
        def read_menu(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()