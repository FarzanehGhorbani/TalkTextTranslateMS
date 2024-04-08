
from typing import List, Union
from typing import Callable, Optional
from typing import Any
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.middleware.base import DispatchFunction
from starlette.types import ASGIApp

from ..proxies.structors import LocalProxy
from ..responses import Response


class ProxyMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        proxies: List[LocalProxy] = [],
        lookupers: List[Callable[[Request], Any]] = [],
        dispatch: DispatchFunction = None,
    ) -> None:
        """_summary_

        Args:
            app (ASGIApp): ...
            proxies (list[LocalProxy], optional): list of proxies. Defaults to [].
            lookupers (list[Callable[[Request], Any]], optional): list of lookupers
            for proxies. Defaults to [].
            dispatch (DispatchFunction, optional): dispatch function.
            Defaults to None.
        """
        super().__init__(app, dispatch)
        self.proxies: list[LocalProxy] = proxies
        self.lookupers: list[Callable[[Request], Any]] = lookupers

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """dispatch function

        Args:
            request (Request): ...
            call_next (RequestResponseEndpoint): ...

        Returns:
            Response: ...
        """
        for idx, proxy in enumerate(self.proxies):
            lookup = None
            if idx in self.lookupers:
                lookup = self.lookupers[idx](request)
            proxy.start(request, lookup=lookup)
        response = await call_next(request)
        return response


