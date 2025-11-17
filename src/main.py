# src/main.py
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount

from src.mcp_app import mcp  # FastMCP インスタンス

async def health(_):
    return PlainTextResponse("ok")

# FastMCP 1.x: HTTP 経由のストリーミング対応 ASGI アプリ
mcp_asgi = mcp.streamable_http_app()

app = Starlette(
    routes=[
        Route("/", health, methods=["GET"]),    # ヘルスチェック
        # 末尾スラッシュの有無どちらでも受ける
        Mount("/mcp",  app=mcp_asgi),
        Mount("/mcp/", app=mcp_asgi),
    ]
)
