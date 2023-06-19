

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import httpx

# from starlette.middleware.sessions import SessionMiddleware
from .config import get_settings
from .views import router as root_router
# from .config import get_settings
# from .auth.exceptions import RequiresLoginException
from .logging import configure_logging
from .data import forwards_data

configure_logging()


@asynccontextmanager
async def lifespan(application: FastAPI):
    # Initialise the Client on startup and add it to the state
    async with httpx.AsyncClient(verify=False) as client:
        yield {'client': client}
        # The Client closes on shutdown


app = FastAPI(title="Webhook Multiplexer", lifespan=lifespan, debug=get_settings().debug)
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
