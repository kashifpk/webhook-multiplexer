
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware
from .config import get_settings
from .views import router as root_router
# from .config import get_settings
# from .auth.exceptions import RequiresLoginException
from .logging import configure_logging
from .data import forwards_data

configure_logging()

app = FastAPI(title="Webhook Multiplexer", debug=get_settings().debug)
# app.add_middleware(SessionMiddleware, secret_key=me.settings.middleware_secret_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

forwards_data.load_data()

app.include_router(root_router)
