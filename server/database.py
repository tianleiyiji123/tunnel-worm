from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

Base = declarative_base()

# Lazy-initialized engine and session factory
_engine = None
_SessionLocal = None


def _create_engine():
    """Create SQLAlchemy engine based on current settings."""
    global _engine, _SessionLocal
    db_type = settings.effective_db_type

    if db_type == "sqlite":
        _engine = create_engine(
            settings.db_url,
            connect_args={"check_same_thread": False},
        )
        print("🗄️ Database: SQLite")
    else:
        _engine = create_engine(
            settings.db_url,
            pool_recycle=3600,
            pool_pre_ping=True,
        )
        print(f"🗄️ Database: MySQL ({settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME})")

    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_engine():
    """Get or create the SQLAlchemy engine (lazy initialization)."""
    if _engine is None:
        _create_engine()
    return _engine


def get_session_local():
    """Get or create the SessionLocal factory (lazy initialization)."""
    if _SessionLocal is None:
        _create_engine()
    return _SessionLocal


class Transfer(Base):
    __tablename__ = "transfer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(4), unique=True, nullable=False, index=True)
    type = Column(String(10), nullable=False)  # text / file / mixed
    text_content = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
    download_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)


class TransferFile(Base):
    __tablename__ = "transfer_file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    transfer_code = Column(String(4), nullable=False, index=True)
    original_name = Column(String(255), nullable=False)
    storage_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(128), nullable=False)


def init_db():
    Base.metadata.create_all(bind=get_engine())


def get_db():
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()
