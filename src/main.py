from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.database.connection import SessionDB, init_db, sessionmanager
from src.config.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix='/api')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def read_root(session: SessionDB):
    await init_db()
    print(session)
    return {"ping": "pong"}
