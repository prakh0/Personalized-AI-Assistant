from .client import MCPClient
from .config import MCP_SERVERS


async def get_all_tools():

    all_tools = []

    for server_name, cfg in MCP_SERVERS.items():

        client = MCPClient(
            command=cfg["command"], args=cfg["args"], env=cfg.get("env", {})
        )

        tools = await client.list_tools()

        print("TOOLS FROM MCP:")
        print(tools)

        for tool in tools:

            all_tools.append(
                {
                    "server": server_name,
                    "name": tool.name,
                    "description": tool.description,
                }
            )

    return all_tools
