import yaml
from fastapi import FastAPI

from src.containers.containers import AppContainer
from src.routers.routers import v1_router
from src.routers.v1 import api as api_routes


def create_app() -> FastAPI:
    with open("./config/config.yml") as fin:
        config = yaml.safe_load(fin)
    container = AppContainer()
    container.config.from_dict(config)
    container.wire([api_routes])
    app = FastAPI()
    set_routers(app)
    return app


def set_routers(app: FastAPI) -> None:
    app.include_router(v1_router)


app = create_app()
