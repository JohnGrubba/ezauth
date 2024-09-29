from fastapi import FastAPI, APIRouter, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from api.signup import router as signupRouter
from api.login import router as loginRouter
from api.internal import router as internalRouter
from api.profile import router as profileRouter
from api.twofactor import router as twofactorRouter
from api.oauth_providers import router as oauthRouter
from api.sessions import router as sessionsRouter
import logging
from api.helpers.extension_loader import load_extensions
from tools import SecurityConfig

__version__ = "0.8.3"

logging.basicConfig(format="%(message)s", level=logging.INFO, force=True)
logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="EZAuth API",
    version=__version__,
    description="""
<img src="https://johngrubba.github.io/ezauth/ezauth_banner.png" />
<h2> EZAuth is a high performance self-hosted and fully customizable authentication service </h2>
""",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=SecurityConfig.access_control_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=SecurityConfig.allow_headers,
)

router = APIRouter(include_in_schema=False)


app.mount("/admin", StaticFiles(directory="admin", html=True, check_dir=False))
app.mount("/cdn", StaticFiles(directory="/uploads", check_dir=False))


@app.middleware("https")
async def mdlware(request: Request, call_next):
    response: Response = await call_next(request)
    if (
        response.status_code == 404
        and "cdn" == request.url.path.split("/")[1]
        and not "default.webp" in request.url.path
    ):
        # Default Profile Pictrue
        return RedirectResponse("/cdn/default.webp", status_code=302)
    return response


@router.get("/")
async def root():
    return RedirectResponse("/docs", status_code=301)


@router.get("/up")
async def up():
    return Response(status_code=204)


app.include_router(router)
app.include_router(signupRouter)
app.include_router(loginRouter)
app.include_router(profileRouter)
app.include_router(sessionsRouter)
app.include_router(twofactorRouter)
app.include_router(oauthRouter)
app.include_router(internalRouter)


load_extensions(app)
logger.info("\u001b[32m--- API Startup Done ---\u001b[0m")
