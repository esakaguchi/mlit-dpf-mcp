# src/main.py

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount

# mcp_app.py で FastMCP インスタンス(mcp)とツール登録をしている前提
from src.mcp_app import mcp

# FastMCP がライフサイクル込みで動く ASGI アプリを生成
# ※ fastmcp のバージョンによってメソッド名が違う場合のフォールバックを用意
try:
    mcp_asgi = mcp.asgi_app()
except AttributeError:
    # 旧版 fastmcp 用のフォールバック（無ければこの import は不要）
    from mcp.server.fastmcp import asgi  # type: ignore
    mcp_asgi = asgi(mcp)  # type: ignore

async def health(request):
    return PlainTextResponse("ok")

# ルート: / → ヘルスチェック, /mcp → FastMCP
app = Starlette(
    routes=[
        Route("/", health),
        Mount("/mcp", app=mcp_asgi),
    ]
)
