import httpx

from src.lib.env_config import Config
import json

async def fetch_mcp_tools(token: str):
    async with httpx.AsyncClient(timeout=30) as client:
        MCP_HEADERS = {
            "Accept": "application/json,text/event-stream",
            "Authorization": f"Bearer {token}"
        }
        payload = {"jsonrpc": "2.0", "id": "1", "method": "tools/list", "params": {}}

        res = await client.post(Config.MCP_SERVER_URL, headers=MCP_HEADERS, json=payload)
        
        # Check if it's SSE format
        if res.text.startswith("event:"):
            # Split lines and find the one starting with 'data: '
            for line in res.text.splitlines():
                if line.startswith("data: "):
                    json_data = json.loads(line[6:]) # Strip 'data: ' prefix
                    return json_data["result"]["tools"]
        
        # Fallback if the server actually sent plain JSON
        data = res.json()
        return data["result"]["tools"]
