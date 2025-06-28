from databricks.sdk import WorkspaceClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_workspace_client():
    w = WorkspaceClient(
        host=os.getenv("DATABRICKS_HOST"),
        client_id=os.getenv("DATABRICKS_CLIENT_ID"),
        client_secret=os.getenv("DATABRICKS_CLIENT_SECRET"),
    )
    return w