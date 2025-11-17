from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from src.mcp_app import mcp

async def health(_):
    return PlainTextResponse("ok")

app = Starlette(
    routes=[
        Route("/", health),
        # ★ FastMCP 0.4 系では asgi_app() ではなく streamable_http_app() を使う
        Mount("/", app=mcp.streamable_http_app()),
    ]
)
