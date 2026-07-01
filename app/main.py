from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(
    title="FreelanceHub API",
    description="API de gestion de projets et clients pour freelances",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": {"code": 500, "message": "Erreur interne du serveur"}},
    )