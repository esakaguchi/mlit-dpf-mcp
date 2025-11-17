# src/main.py
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from src.mcp_app import mcp   # FastMCP インスタンス

async def health(_):
    return PlainTextResponse("ok")

# FastMCP 1.x: HTTP ストリーミング ASGI アプリ（POST専用エンドポイント）
http_app = mcp.streamable_http_app()

app = Starlette(
    routes=[
        # まず /mcp を HTTP版 MCP に割り当て（/mcp と /mcp/ の両方を受ける）
        Mount("/mcp",  app=http_app),
        Mount("/mcp/", app=http_app),

        # ルートのヘルスチェック（GET のみ）
        Route("/", health, methods=["GET"]),
    ]
)
