from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def read_root():
    """
    Root endpoint.
    """
    return {"message": "Hello World"}


@router.get("/v1/status")
async def status():
    """
    Get the status of the API.
    """
    return {"message": "running"}
