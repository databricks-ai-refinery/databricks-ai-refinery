from databricks.sdk import WorkspaceClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_workspace_client():
    w = WorkspaceClient()
    return w

def run_query_attachments(workspace_client, space_id, response):
    # print("\nRunning query:", response.attachments[0].query)
    query_result = workspace_client.genie.get_message_attachment_query_result(space_id, 
                                                                                response.conversation_id, 
                                                                                response.id, 
                                                                                response.attachments[0].attachment_id)
    # print("\nRaw query result:", query_result)
    return query_result.statement_response.result.data_array

def start_genie_conversation(workspace_client, space_id, message):
    response = workspace_client.genie.start_conversation_and_wait(
        space_id=space_id,
        content=message,
    )
    if response.attachments[0].query:
        raw_output = run_query_attachments(workspace_client, space_id, response)
    else:
        raw_output = []
    return response, raw_output

def continue_genie_conversation(workspace_client,
                                space_id,
                                conversation_id,
                                content):
    response = workspace_client.genie.create_message_and_wait(space_id,
                                                              conversation_id,
                                                              content)
    if response.attachments[0].query:
        raw_output = run_query_attachments(workspace_client, space_id, response)
    else:
        raw_output = []
    return response, raw_output

if __name__ == "__main__":
    SPACE_ID = os.getenv("GENIE_SPACE_ID")

    queries = [
        "List and describe the tables in this data set",
        # "What information does the first column of the first table include?",
        "How many rows does the first table have?",
        # "Which agents handled the most top priority tickets?",
        "Show me the first ten rows of the first table",
        # "How many top priority tickets did Kristos Westoll handle?",
        # "What is the total number of top priority tickets handled?"
        # "What are the levels of priority shown for the tickets?"
        ]

    client = get_workspace_client()
    print("WorkspaceClient successfully initialized with authentication token.")
    
    for i, query in enumerate(queries):
        if i == 0:
            print("\n\nUser query: ", query)
            genie_response, text_out = start_genie_conversation(client, SPACE_ID, query)
            if len(text_out) > 0:
                print("\n--- Agent Response:")
                # print(*sql_out, sep="\n")
                for row in sql_out:
                    print(' '.join(map(str,row)))
            else:
                print("\n--- Agent Response:", genie_response.attachments[0].text.content)
            # print("\n\n--- Agent Response:", genie_response)
        else:
            print("\n\nUser query: ", query)
            genie_response, sql_out = continue_genie_conversation(client,
                                                        space_id=SPACE_ID, 
                                                        conversation_id=genie_response.conversation_id, 
                                                        content=query)    
            if len(sql_out) > 0:
                print("\n--- Agent Response:")
                # print(*sql_out, sep="\n")
                for row in sql_out:
                    print(' '.join(map(str,row)))
            else:
                print("\n--- Agent Response:", genie_response.attachments[0].text.content)
            # print("\n\n--- Agent Response:", genie_response)
