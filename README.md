# databricks-ai-refinery

By combining the power of the [Databricks Mosaic AI](https://www.databricks.com/product/artificial-intelligence#related-products) and [Accenture AI Refinery](https://sdk.airefinery.accenture.com/setup/ai_refinery_101/), 
you unlock a wide range of agentic capabilities that supercharge your business applications.

##### Key Benefits:

- Leverage **data** stored in the Databricks Lakehouse and Lakebase within your AI Refinery agentic applications
- Leverage AI Refinery **pre-built components** in Mosaic AI agents
- Add **enterprise governance** to AI Refinery applications using Unity Catalog for managing data and agentic tools
- Use Databricks Apps to build **front-ends** for AI Refinery agents rapidly in a governed way
- Interact with AI Refinery agents using **Genie**
- Use Databricks **Vector Search** in AI Refinery agents
- Access AI Refinery agents through the Mosaic AI **Playground**
- Use Databricks managed and custom **MCP servers** in AI Refinery agents 
- Use **AI Bricks** to orchestrate AI Refinery agents using the multi-agent orchestrator
- Implement real-time ingestion using Zerobus from **physical devices** such as cameras and sensors
- Build Brickbuilder **industry solutions** using AI Refinery components


##### Authentication

Here is how you can authenticate to Databricks using a [service principal](https://docs.databricks.com/aws/en/dev-tools/auth/oauth-m2m?language=Python) (M2M). Note that it is also possible to set up User-based authentication (U2M) using Oauth2.

###### Step 1: Create a service principal

<img src="media/service-principal-permissions.png" width="800px">


###### Step 2: Generate a secret

<img src="media/service-principal-secrets.png" width="800px">


###### Step 3: Set up a .env file with the following environment variables

```
DATABRICKS_HOST
DATABRICKS_CLIENT_ID
DATABRICKS_CLIENT_SECRET
```


###### Step 4: Login using the Databricks Python SDK

```python
from databricks_helper import get_workspace_client
w = get_workspace_client()
```

