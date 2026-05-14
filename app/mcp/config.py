import os
from dotenv import load_dotenv

load_dotenv()

MCP_SERVERS = {
    "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GIT_TOKEN")},
    }
}
