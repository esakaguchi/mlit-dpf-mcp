# src/main.py
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from src.mcp_app import mcp

async def health(_):
    return PlainTextResponse("ok")

# mcp.streamable_http_app() が /mcp（既定）を含むHTTPエンドポイント群を生やします
app = Starlette(
    routes=[
        Route("/", health),
        Mount("/", app=mcp.streamable_http_app()),
    ]
)
