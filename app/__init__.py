
from . import highlights
from . import session
from . import routes

from .logging import Console, File

from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError

from fastapi import (
    HTTPException,
    Response,
    Request,
    FastAPI
)

import logging
import uvicorn
import config
import utils
import time

utils.setup()

logging.basicConfig(
    format='[%(asctime)s] - <%(name)s> %(levelname)s: %(message)s',
    level=logging.INFO,
    handlers=[Console, File]
)

if logging.getLogger('uvicorn.access').handlers:
    # Redirect uvicorn logs to file
    logging.getLogger('uvicorn.access').addHandler(File)
    logging.getLogger('uvicorn.error').addHandler(File)

api = FastAPI(
    title='Deck',
    description='API for osu! clients',
    version=config.VERSION,
    redoc_url=None,
    docs_url=None,
    debug=True if config.DEBUG else False
)

@api.middleware('http')
def get_process_time(request: Request, call_next):
    start = time.time()
    response = call_next(request)
    total_time = time.time() - start
    session.logger.debug(
        f'Processing Time: ~{round(total_time, 4)} seconds'
    )
    return response

@api.exception_handler(HTTPException)
def exception_handler(request: Request, exc: HTTPException):
    headers = exc.headers if exc.headers else {}
    headers.update({'detail': exc.detail})

    return Response(
        status_code=exc.status_code,
        headers=headers
    )

@api.exception_handler(StarletteHTTPException)
def exception_handler(request: Request, exc: StarletteHTTPException):
    return Response(
        status_code=exc.status_code,
        headers={'detail': exc.detail}
    )

@api.exception_handler(RequestValidationError)
def validation_error(request: Request, exc: RequestValidationError):
    return Response(
        status_code=400,
        content='no'
    )

api.include_router(routes.router)

def run():
    uvicorn.run(
        api,
        host=config.WEB_HOST,
        port=config.WEB_PORT,
        log_config=None
    )
