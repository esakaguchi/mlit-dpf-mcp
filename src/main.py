# src/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

# Vercel (@vercel/python) は module-level に `app` を探します
app = FastAPI()

@app.get("/")
def health():
    # ここが表示されれば FastAPI は起動OK
    return PlainTextResponse("ok")

@app.post("/mcp")
async def mcp_http(req: Request):
    # まずは到達確認用のエコー返し
    try:
        body = await req.json()
    except Exception:
        body = None
    return JSONResponse({"status": "running", "echo": body})
