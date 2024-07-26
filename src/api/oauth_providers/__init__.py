from fastapi import APIRouter
from tools import SignupConfig

router = APIRouter(
    prefix="/oauth",
    tags=["OAuth"],
    dependencies=[],
)

if "google" in SignupConfig.oauth_providers:
    from .google import router as ggl

    router.include_router(ggl)
if "github" in SignupConfig.oauth_providers:
    from .github import router as gh

    router.include_router(gh)
