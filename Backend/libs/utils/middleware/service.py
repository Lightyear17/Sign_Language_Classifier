import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from libs.utils.logger import request_id_var, request_path_var


class ServiceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Generate a unique request ID and store the request path
        request_id_var.set(str(uuid.uuid4()))
        request_path_var.set(request.url.path)
        return await call_next(request)
