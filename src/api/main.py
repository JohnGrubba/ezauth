from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from api.signup import router as signupRouter
import logging

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

app = FastAPI(
    title="EZAuth API",
    description="""
<img src="https://johngrubba.github.io/ezauth/ezauth_banner.png" />
<h2> EZAuth is a high performance self-hosted and fully customizable authentication service </h2>
""",
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(include_in_schema=False)


@router.get("/")
async def root():
    return RedirectResponse("/docs", status_code=301)


app.include_router(router)
app.include_router(signupRouter)
