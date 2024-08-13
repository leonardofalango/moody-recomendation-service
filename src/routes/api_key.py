from fastapi import status, Request
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv

load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
_API_KEY = os.environ["API_KEY"]


async def api_key_middleware(request: Request, call_next):
    api_key = request.headers.get("X-API-KEY")
    if api_key != _API_KEY:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Invalid API Key"},
        )

    response = await call_next(request)
    return response
