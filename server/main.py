from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from database import init_db, get_session_local
from services import transfer_service
from routes.transfer import router as transfer_router
from routes.setup import router as setup_router
from routes.auth import router as auth_router
from routes.records import router as records_router

# Frontend static files directory (Docker: /app/static, dev: not used)
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

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

    # Ensure JWT_SECRET is set
    from config import settings, CONFIG_FILE
    if not settings.JWT_SECRET:
        import json, secrets
        jwt_secret = secrets.token_urlsafe(32)
        # Write to config.json
        cfg = {}
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                cfg = json.load(f)
        cfg["JWT_SECRET"] = jwt_secret
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
        settings.JWT_SECRET = jwt_secret
        print("🔑 Generated JWT secret")

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
app.include_router(auth_router)
app.include_router(records_router)
app.include_router(transfer_router)


@app.get("/api/health")
async def health_check():
    from setup_config import is_initialized
    return {"status": "ok", "service": "suisuichong", "initialized": is_initialized()}


# Serve frontend static files (only in Docker / production)
if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# SPA catch-all: return index.html for any non-API, non-static path
@app.get("/{path:path}")
async def spa_catchall(request: Request, path: str):
    """Serve index.html for client-side routing (Vue Router history mode)."""
    index_path = STATIC_DIR / "index.html"
    if index_path.is_file():
        return FileResponse(str(index_path))
    return {"error": "Frontend not found. Run 'npm run build' in client/ or use Docker."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7895, reload=True, log_level="info")

