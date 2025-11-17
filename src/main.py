from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from src.mcp_app import mcp

async def health(_):
    return PlainTextResponse("ok")

app = Starlette(
    routes=[
        Route("/", health),
        # FastMCP 1.x では streamable_http_app() を使う
        Mount("/mcp", app=mcp.streamable_http_app()),
    ]
)
