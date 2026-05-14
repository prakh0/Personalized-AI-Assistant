from .client import MCPClient
from .config import MCP_SERVERS


async def execute_mcp_tool(server_name, tool_name, arguments):

    cfg = MCP_SERVERS[server_name]

    client = MCPClient(command=cfg["command"], args=cfg["args"], env=cfg.get("env", {}))

    result = await client.call_tool(tool_name, arguments)

    return result
