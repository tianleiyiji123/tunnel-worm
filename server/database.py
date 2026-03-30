from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index, func
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


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


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
    # User system fields
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    permanent = Column(Boolean, default=False, server_default="0")


class TransferFile(Base):
    __tablename__ = "transfer_file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    transfer_code = Column(String(4), nullable=False, index=True)
    original_name = Column(String(255), nullable=False)
    storage_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    content_type = Column(String(128), nullable=False)


class TransferRecord(Base):
    __tablename__ = "transfer_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    action = Column(String(10), nullable=False)  # send / retrieve
    transfer_code = Column(String(4), nullable=False, index=True)
    client_ip = Column(String(45), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_record_user_time", "user_id", "created_at"),
    )


def init_db():
    Base.metadata.create_all(bind=get_engine())


def get_db():
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()
