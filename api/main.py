from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes import homework

from exceptions.exceptions import BotodomApiError, BadRequest, NotFound
from exceptions.handlers import create_exception_handler
from fastapi import Request, status
from typing import Callable
from routes import verification




app = FastAPI(
    title="Botodom API",
    summary="Botodom API",
)

@app.exception_handler(500)
async def internalServerError(request, exc):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal Server Error"},
    )


app.add_exception_handler(
    exc_class_or_status_code=BotodomApiError,
    handler=create_exception_handler(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "An error occurred in the AlertaRiscos API."
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=BadRequest,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST,
        "BadRequest"
    ),
)

app.add_exception_handler(
    exc_class_or_status_code=NotFound,
    handler=create_exception_handler(
        status.HTTP_404_NOT_FOUND,
        "NotFound"
    ),
)

app.include_router(homework.router)
app.include_router(verification.router)

