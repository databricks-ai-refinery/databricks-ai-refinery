import asyncio, os
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
from databricks_mcp import DatabricksOAuthClientProvider
from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv
load_dotenv()

# TODO: Update to the Databricks CLI profile name you specified when
# configuring authentication to the workspace.
databricks_config_profile = os.getenv("DATABRICKS_CONFIG_PROFILE")
genie_space_id = os.getenv("GENIE_SPACE_ID")
assert (
    databricks_config_profile is not None
), "Set databricks_config_profile to the Databricks CLI profile name you specified when configuring authentication to the workspace"
workspace_client = WorkspaceClient(profile=databricks_config_profile)
workspace_hostname = workspace_client.config.host
mcp_server_url = f"{workspace_hostname}/api/2.0/mcp/genie/{genie_space_id}"


# This snippet below uses the Unity Catalog functions MCP server to expose built-in
# AI tools under `system.ai`, like the `system.ai.python_exec` code interpreter tool
async def call_genie(query):
    async with streamablehttp_client(
        f"{mcp_server_url}", auth=DatabricksOAuthClientProvider(workspace_client)
    ) as (read_stream, write_stream, _), ClientSession(
        read_stream, write_stream
    ) as session:
        # List and call tools from the MCP server
        await session.initialize()
        # tools = await session.list_tools()
        # print(
        #     f"Discovered tools {[t.name for t in tools.tools]} "
        #     f"from MCP server {mcp_server_url}\n\n"
        # )
        result = await session.call_tool(
            f"query_space_{genie_space_id}", {"query": query}
        )
        result_text = result.content[0].text
        return result_text

# Command line interface
# pip install fire
import fire

def genie(query="What tables are there and how are they connected? Give me a short summary."):
    result_text = asyncio.run(call_genie(query))
    print(result_text)

if __name__ == "__main__":
    fire.Fire(genie)
