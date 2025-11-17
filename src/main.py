from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount
from src.mcp_app import mcp  # ← あなたの mcp_app を読み込む

async def health(_):
    return PlainTextResponse("ok")

# / にヘルス、/mcp は FastMCP の HTTP（Streamable HTTP）
app = Starlette(
    routes=[
        Route("/", health),
        Mount("/", app=mcp.streamable_http_app()),
    ]
)
