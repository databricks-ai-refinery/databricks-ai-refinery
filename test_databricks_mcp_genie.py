import asyncio

from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
from databricks_mcp import DatabricksOAuthClientProvider
from databricks.sdk import WorkspaceClient

import os
from dotenv import load_dotenv
load_dotenv()
genie_space_id = os.getenv("GENIE_SPACE_ID")

# NOTE: You need to pin the mcp version to mcp==1.9.4 in requirements.txt 
# for this script to work

# TODO: Update to the Databricks CLI profile name you specified when
# configuring authentication to the workspace.
databricks_cli_profile = "enb-accenture"
assert (
    databricks_cli_profile != "YOUR_DATABRICKS_CLI_PROFILE"
), "Set databricks_cli_profile to the Databricks CLI profile name you specified when configuring authentication to the workspace"
workspace_client = WorkspaceClient(profile=databricks_cli_profile)
workspace_hostname = workspace_client.config.host
mcp_server_url = f"{workspace_hostname}/api/2.0/mcp/genie/{genie_space_id}"


# This snippet below uses the Unity Catalog functions MCP server to expose built-in
# AI tools under `system.ai`, like the `system.ai.python_exec` code interpreter tool
async def test_connect_to_server():
    async with streamablehttp_client(
        f"{mcp_server_url}", auth=DatabricksOAuthClientProvider(workspace_client)
    ) as (read_stream, write_stream, _), ClientSession(
        read_stream, write_stream
    ) as session:
        # List and call tools from the MCP server
        await session.initialize()
        tools = await session.list_tools()
        print(
            f"Discovered tools {[t.name for t in tools.tools]} "
            f"from MCP server {mcp_server_url}"
        )


if __name__ == "__main__":
    asyncio.run(test_connect_to_server())