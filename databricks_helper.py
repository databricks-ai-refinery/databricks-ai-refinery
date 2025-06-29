from databricks.sdk import WorkspaceClient
import os
from dotenv import load_dotenv

# NOTE: You need to pin the mcp version to mcp==1.9.4 in requirements.txt 
# for this script to work

load_dotenv()

def get_workspace_client():
    w = WorkspaceClient(
        host=os.getenv("DATABRICKS_HOST"),
        client_id=os.getenv("DATABRICKS_CLIENT_ID"),
        client_secret=os.getenv("DATABRICKS_CLIENT_SECRET"),
    )
    return w

def list_genie_spaces(workspace_client):
    spaces = workspace_client.genie.list_spaces()
    return spaces

def start_genie_conversation(workspace_client, 
                             space_id = os.getenv("GENIE_SPACE_ID"), 
                             message: str = "List and describe the tables in this data set"):
    response = workspace_client.genie.start_conversation_and_wait(
        space_id=space_id,
        content=message,
    )
    return response