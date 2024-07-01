from fastapi import APIRouter, Header, HTTPException, Depends
from typing import Annotated
from tools.conf import InternalConfig


async def check_internal_key(internal_api_key: Annotated[str, Header()]):
    if not internal_api_key:
        raise HTTPException(status_code=401)
    if internal_api_key != InternalConfig.internal_api_key:
        raise HTTPException(status_code=401)


router = APIRouter(
    prefix="/internal",
    tags=["Internal API"],
    dependencies=[Depends(check_internal_key)],
    responses={401: {"description": "Unauthorized"}},
)


@router.get("/health")
async def health():
    """
    # Check Health / API Key

    ## Description
    This endpoint is used to check the health of the API and the API Key.
    Can also be used to check if `/internal` endpoints are blocked from public access.
    """
    return {"status": "ok"}


@router.post("/broadcast-email")
async def broadcast_email():
    """
    # Broadcast a E-Mail Template to all Users

    ## Description
    This endpoint is used to broadcast a E-Mail Template to all users.
    """
    return {"status": "ok"}
