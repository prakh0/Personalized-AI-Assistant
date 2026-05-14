from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:

    def __init__(self, command, args, env=None):

        self.command = command
        self.args = args
        self.env = env or {}

    async def list_tools(self):

        server_params = StdioServerParameters(
            command=self.command, args=self.args, env=self.env
        )

        async with stdio_client(server_params) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                response = await session.list_tools()

                return response.tools

    async def call_tool(self, tool_name, arguments):

        server_params = StdioServerParameters(
            command=self.command, args=self.args, env=self.env
        )

        async with stdio_client(server_params) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                result = await session.call_tool(tool_name, arguments)

                return result
