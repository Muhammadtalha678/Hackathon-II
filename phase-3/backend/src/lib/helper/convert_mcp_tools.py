from agents import function_tool, RunContextWrapper
import httpx

from src.lib.env_config import Config
def convert_mcp_tools(mcp_tools, token: str):

    tools = []

    for tool in mcp_tools:
        name = tool["name"]
        description = tool.get("description", "")
        parameters = tool.get("input_schema", {})

        async def tool_func(ctx: RunContextWrapper, tool_name=name, **kwargs):
            async with httpx.AsyncClient(timeout=30) as client:
                payload = {
                    "jsonrpc": "2.0",
                    "id": "tool-call",
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": kwargs
                    }
                }

                headers = {
                    "Accept": "application/json,text/event-stream",
                    "Authorization": f"Bearer {token}"
                }

                res = await client.post(
                    Config.MCP_SERVER_URL,
                    headers=headers,
                    json=payload
                )

                return res.json()

        tools.append(
            function_tool(
                name=name,
                description=description,
                parameters=parameters,
                func=tool_func
            )
        )

    return tools
