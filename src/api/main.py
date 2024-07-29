from fastapi import FastAPI, APIRouter, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from api.signup import router as signupRouter
from api.login import router as loginRouter
from api.internal import router as internalRouter
from api.profile import router as profileRouter
from api.twofactor import router as twofactorRouter
from api.oauth_providers import router as oauthRouter
from api.sessions import router as sessionsRouter
import logging
import os
import importlib
import importlib.util
from tools import SecurityConfig

logging.basicConfig(format="%(message)s", level=logging.INFO, force=True)
logger = logging.getLogger("uvicorn")

app = FastAPI(
    title="EZAuth API",
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


def load_extensions():
    # Extension Loading
    extensions_dir = "/src/app/extensions/"
    if not os.path.exists(extensions_dir):
        return
    modules = []
    for item in os.listdir(extensions_dir):
        item_path = os.path.join(extensions_dir, item)
        init_file = os.path.join(item_path, "__init__.py")
        if os.path.isdir(item_path) and os.path.isfile(init_file):
            spec = importlib.util.spec_from_file_location(item, init_file)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                logger.error(f"Failed to load extension {item}: {e}")
                if logger.level == logging.INFO:
                    raise e
                continue
            modules.append([spec, module])

    for spec, module in modules:
        app.include_router(module.router, prefix=f"/ext/{module.__name__}")

    logger.info(
        "\u001b[32m-> Loaded Extensions: "
        + ", ".join([module.__name__ for spec, module in modules])
        + "\u001b[0m"
    )


load_extensions()
logger.info("\u001b[32m--- API Startup Done ---\u001b[0m")
