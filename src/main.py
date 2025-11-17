from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from src.mcp_app import mcp

async def health(_):
    return PlainTextResponse("ok")

app = Starlette(
    routes=[
        Route("/", health),
        Mount("/", app=mcp.streamable_http_app()),
    ]
)
