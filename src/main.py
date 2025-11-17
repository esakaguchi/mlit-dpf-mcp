# src/main.py
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from src.mcp_app import mcp  # FastMCP インスタンス

async def health(_):
    return PlainTextResponse("ok")

# FastMCP 1.x: streamable_http_app() を使う
mcp_asgi = mcp.streamable_http_app()

app = Starlette(
    routes=[
        Route("/", health),                    # GET /
        Mount("/mcp", app=mcp_asgi),           # POST /mcp で MCP
    ]
)
