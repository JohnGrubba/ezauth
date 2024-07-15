from fastapi import FastAPI, APIRouter, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from api.signup import router as signupRouter
from api.login import router as loginRouter
from api.internal import router as internalRouter
from api.profile import router as profileRouter
from api.twofactor import router as twofactorRouter
from api.oauth_providers import router as oauthRouter
import logging
from tools import AccessConfig

logging.basicConfig(format="%(message)s", level=logging.INFO, force=True)

app = FastAPI(
    title="EZAuth API",
    description="""
<img src="https://johngrubba.github.io/ezauth/ezauth_banner.png" />
<h2> EZAuth is a high performance self-hosted and fully customizable authentication service </h2>
""",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=AccessConfig.access_control_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=AccessConfig.allow_headers,
)

router = APIRouter(include_in_schema=False)


@router.get("/")
async def root():
    return RedirectResponse("/docs", status_code=301)


@router.get("/up")
async def up():
    return Response(status_code=204)


app.include_router(router)
app.include_router(signupRouter)
app.include_router(loginRouter)
app.include_router(internalRouter)
app.include_router(profileRouter)
app.include_router(twofactorRouter)
app.include_router(oauthRouter)
