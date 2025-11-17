# src/mcp_app.py
from typing import Optional
from mcp.server.fastmcp import FastMCP
from src.client import MLITClient

mcp = FastMCP("mlit-mcp")

# まずは疎通確認用の最小ツール
@mcp.tool()
def ping() -> dict:
    """ヘルスチェック用"""
    return {"ok": True}

@mcp.tool()
async def search(
    term: str = "",
    first: int = 0,
    size: int = 50,
    phrase_match: bool = True,
    # ↓ ここを Optional[str] にする（PEP604 は使わない）
    sort_attribute_name: Optional[str] = None,
    sort_order: Optional[str] = None,
    minimal: bool = False,
) -> dict:
    """
    MLIT DPF のキーワード検索
    """
    client = MLITClient()
    try:
        fields = client._fields_min() if minimal else client._fields_basic()
        data = await client.search_keyword(
            term=term or "",
            first=first,
            size=size,
            phrase_match=phrase_match,
            sort_attribute_name=sort_attribute_name,
            sort_order=sort_order,
            fields=fields,
        )
        return data
    finally:
        await client.close()
