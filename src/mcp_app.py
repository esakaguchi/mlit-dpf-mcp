# src/mcp_app.py
from mcp.server.fastmcp import FastMCP
from src.client import MLITClient

mcp = FastMCP("mlit-mcp")  # サーバ名は任意

@mcp.tool()
async def search(
    term: str = "",
    first: int = 0,
    size: int = 50,
    phrase_match: bool = True,
    sort_attribute_name: str | None = None,
    sort_order: str | None = None,
    minimal: bool = False,
):
    """
    MLIT DPF のキーワード検索。ChatGPT がこのツールを自動で使います。
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
        return data  # FastMCP は dict/配列をそのまま JSON として返せます
    finally:
        await client.close()
