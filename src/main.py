from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI()

@app.get("/")
def read_root():
    return PlainTextResponse("ok")

@app.post("/mcp")
async def handle_mcp(req: Request):
    body = await req.json()
    return JSONResponse({"status": "running", "echo": body})
