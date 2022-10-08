import sqlalchemy as _sql
import sqlalchemy.orm as _orm

DATABASE_URL = "sqlite:///./database.db"

engine = _sql.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = _orm.session.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _orm.declarative_base()


def create_database():
    import models

    return Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
