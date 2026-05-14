from fastapi import FastAPI
import json

from app.mcp.connect import get_all_tools
from app.mcp.xyz import execute_mcp_tool

app = FastAPI()


@app.get("/")
async def root():

    return {"message": "MCP initialized"}


@app.get("/tools")
async def tools():

    return await get_all_tools()


@app.get("/search")
async def search_repo(query: str):

    result = await execute_mcp_tool(
        server_name="github",
        tool_name="search_repositories",
        arguments={"query": query},
    )

    data = json.loads(result.content[0].text)

    repos = []

    for repo in data["items"][:10]:

        repos.append(
            {
                "name": repo["full_name"],
                "description": repo["description"],
                "url": repo["html_url"],
            }
        )

    return repos
