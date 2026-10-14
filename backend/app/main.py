import logging
import re
import uuid

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.db import check_database
from app.logging_setup import request_id_var, setup_logging

settings = get_settings()
setup_logging(settings.log_level)
log = logging.getLogger("sentineliq.api")

app = FastAPI(title="SentinelIQ API", version="0.1.0")

# Only accept short, simple client-supplied IDs; anything else is replaced.
# This stops log injection through the header.
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9-]{1,64}$")


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    supplied = request.headers.get("X-Request-ID", "")
    rid = supplied if REQUEST_ID_PATTERN.match(supplied) else str(uuid.uuid4())
    token = request_id_var.set(rid)
    try:
        response = await call_next(request)
        log.info("%s %s %s", request.method, request.url.path, response.status_code)
    finally:
        request_id_var.reset(token)
    response.headers["X-Request-ID"] = rid
    return response


router = APIRouter(prefix="/api/v1")


@router.get("/health/live")
def live():
    return {"status": "ok"}


@router.get("/health/ready")
def ready():
    if check_database():
        return {"status": "ready"}
    return JSONResponse(status_code=503, content={"status": "database_unavailable"})


app.include_router(router)
