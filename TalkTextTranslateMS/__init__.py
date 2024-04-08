from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from pydantic_settings import BaseSettings

from .core import (
    BaseResponse,
    ProxyMiddleware,
    request,
    message,
)


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)


class Application:
    app: FastAPI = ...  # type: ignore
    translated_speech_result: str|None = None
    # Other extenssions
    # mongo
    # jwt
    # redis
    # socket


def create_app(config: BaseSettings) -> FastAPI:  # type: ignore
    root = Application

    root.config = config.dict()  # type: ignore

    root.app = FastAPI(
        debug=root.config.get("DEBUG", True),  # type: ignore
        title="Video Content Service",
        swagger_ui_parameters={"displayRequestDuration": True},
        default_response_class=BaseResponse,
    )
    root.app.add_middleware(
        CORSMiddleware,
        allow_origins=root.config.get("ALLOWED_HOSTS", "*"),  # type: ignore
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    root.app.add_middleware(
        ProxyMiddleware,
        proxies=[request, message],
        lookupers=[lambda request: request],
    )

    from .controllers.views import router

    root.app.include_router(router)

    return root.app
