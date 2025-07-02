from databricks.sdk import WorkspaceClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_workspace_client():
    w = WorkspaceClient(
        host=os.getenv("DB_HOST"),
        token=os.getenv("DB_TOKEN"),
    )
    return w

def start_genie_conversation(workspace_client, space_id, message):
    response = workspace_client.genie.start_conversation_and_wait(
        space_id=space_id,
        content=message,
    )
    return response

def continue_genie_conversation(workspace_client,
                                space_id,
                                conversation_id,
                                content):
    response = workspace_client.genie.create_message_and_wait(space_id,
                                                              conversation_id,
                                                              content)
    return response

if __name__ == "__main__":
    SPACE_ID = os.getenv("GENIE_SPACE_ID")

    queries = ["List and describe the tables in this data set",
               "What information does the first column of the first table include?"]

    client = get_workspace_client()
    print("WorkspaceClient successfully initialized with authentication token.")
    
    for i, query in enumerate(queries):
        if i == 0:
            print("\nUser query: ", query)
            genie_response = start_genie_conversation(client, SPACE_ID, query)
            print("\n\n--- Agent Response:", genie_response.attachments[0].text.content)
        else:
            print("\nUser query: ", query)
            genie_response = continue_genie_conversation(client,
                                                        space_id=SPACE_ID, 
                                                        conversation_id=genie_response.conversation_id, 
                                                        content=query)    
            print("\n\n--- Agent Response:", genie_response.attachments[0].text.content)
