# src/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
import importlib
import inspect
import asyncio
from typing import Any, Callable, Optional

app = FastAPI()

@app.get("/")
def health():
    return PlainTextResponse("ok")

def _find_mcp_handler() -> Optional[Callable[[dict], Any]]:
    """
    server.py 内の MCP HTTP ハンドラを色々な名前で探す。
    - 関数: handle_http, http_handle
    - オブジェクト: server / app / mcp に handle_http がある
    - クラス: Server/MCPServer/MLITServer のインスタンスを作って handle_http
    """
    try:
        mod = importlib.import_module("src.server")
    except Exception:
        # プロジェクトによっては top-level が "server" のこともある
        try:
            mod = importlib.import_module("server")
        except Exception:
            return None

    # 1) 関数として直接エクスポート
    for name in ["handle_http", "http_handle"]:
        fn = getattr(mod, name, None)
        if callable(fn):
            return fn

    # 2) オブジェクトが持つメソッド
    for obj_name in ["server", "app", "mcp"]:
        obj = getattr(mod, obj_name, None)
        if obj is not None:
            fn = getattr(obj, "handle_http", None)
            if callable(fn):
                # バウンドメソッドとして返す
                return fn

    # 3) クラスを見つけてインスタンス化してメソッド呼び出し
    for cls_name in ["Server", "MCPServer", "MLITServer"]:
        cls = getattr(mod, cls_name, None)
        if inspect.isclass(cls):
            try:
                inst = cls()  # 引数なしコンストラクタ前提
                fn = getattr(inst, "handle_http", None)
                if callable(fn):
                    return fn
            except Exception:
                pass

    return None

_HANDLER = _find_mcp_handler()

@app.post("/mcp")
async def mcp_http(req: Request):
    body = await req.json()

    if _HANDLER is None:
        # タイムアウトを避けるため即時エラー（何が足りないかヒントを返す）
        return JSONResponse(
            {
                "error": "MCP handler not found in src/server.py",
                "tried": [
                    "handle_http()", "http_handle()",
                    "server.handle_http()", "app.handle_http()", "mcp.handle_http()",
                    "Server().handle_http()", "MCPServer().handle_http()", "MLITServer().handle_http()"
                ],
                "hint": "src/server.py に HTTP用のハンドラ関数(またはメソッド) 'handle_http' を用意してください。"
            },
            status_code=400
        )

    try:
        if inspect.iscoroutinefunction(_HANDLER):
            result = await _HANDLER(body)
        else:
            # 同期関数にも対応
            result = await asyncio.to_thread(_HANDLER, body)

        # 返り値は MCPプロトコルのHTTPレスポンス(JSON)を想定
        return JSONResponse(result)
    except Exception as e:
        # 失敗時も即時JSONを返してChatGPT側のタイムアウトを防止
        return JSONResponse(
            {"error": "handler_execution_failed", "detail": str(e)},
            status_code=500
        )
