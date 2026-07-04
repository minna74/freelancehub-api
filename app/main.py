import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import auth, clients, projects, tasks

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)
logger = logging.getLogger("freelancehub")

app = FastAPI(
    title="FreelanceHub API",
    description="API de gestion de projets et clients pour freelances",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)

    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {duration_ms}ms"
    )

    return response


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": {"code": 500, "message": "Erreur interne du serveur"}},
    )