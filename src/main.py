# src/main.py
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from src.mcp_app import mcp

async def health(_):
    return PlainTextResponse("ok")

app = Starlette(
    routes=[
        # ヘルスチェック
        Route("/", health, methods=["GET"]),
        Route("/mcp", health, methods=["GET"]),   # ChatGPT の疎通チェック用

        # MCP は /mcp 配下で受ける（POST /mcp など）
        Mount("/mcp", app=mcp.streamable_http_app()),
    ]
)
