from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from database import init_db, get_session_local
from services import transfer_service
from routes.transfer import router as transfer_router
from routes.setup import router as setup_router

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - lazy init storage
    from services.storage import get_storage
    storage = get_storage()
    storage_type_name = type(storage).__name__.replace("Storage", "").lower()
    print(f"🚀 SuiSuiChong starting up... (storage: {storage_type_name})")

    # Ensure data directory exists
    from config import DATA_DIR
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    init_db()
    await storage.ensure_bucket()
    print("✅ Database initialized")
    print("✅ Storage backend ready")

    # Cleanup expired transfers on startup
    db = get_session_local()()
    try:
        transfer_service.cleanup_expired(db)
    finally:
        db.close()

    # Schedule periodic cleanup (every hour)
    scheduler.add_job(
        periodic_cleanup,
        "interval",
        hours=1,
        id="cleanup_expired",
    )
    scheduler.start()
    print("✅ Scheduled cleanup task (every hour)")

    yield

    # Shutdown
    scheduler.shutdown()
    print("👋 SuiSuiChong shutting down...")


def periodic_cleanup():
    db = get_session_local()()
    try:
        transfer_service.cleanup_expired(db)
    finally:
        db.close()


app = FastAPI(
    title="隧隧虫",
    description="跨设备资源传输工具",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS - allow all origins in dev, restricted in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(setup_router)
app.include_router(transfer_router)


@app.get("/api/health")
async def health_check():
    from setup_config import is_initialized
    return {"status": "ok", "service": "suisuichong", "initialized": is_initialized()}
