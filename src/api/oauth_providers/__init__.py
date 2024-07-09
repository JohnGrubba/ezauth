from fastapi import APIRouter
import importlib
from tools.conf import SignupConfig

router = APIRouter(
    prefix="/oauth",
    tags=["OAuth"],
    dependencies=[],
)


if "google" in SignupConfig.oauth_providers:
    from .google import router as ggl

    router.include_router(ggl)
