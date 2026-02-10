import os
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import Tool, TextContent

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings

# -----------------------------------------------------------------------
# Setup the MCP Server
# -----------------------------------------------------------------------
load_dotenv()
server = Server("HR-Policies-MCP-Server")

# -----------------------------------------------------------------------
# Setup the Vector Store for use in retrieving policies
# This will use the hr_policy_document.pdf file as its source
# -----------------------------------------------------------------------

pdf_filename = "hr_policy_document.pdf"
pdf_full_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), pdf_filename))

# Load and split the PDF document
loader = PyPDFLoader(pdf_full_path)
policy_documents = loader.load_and_split()

# Create embeddings
policy_embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create In memory vector store
policy_vector_store = InMemoryVectorStore.from_documents(
    policy_documents, policy_embeddings)

# -----------------------------------------------------------------------
# Setup the MCP tool to query for policies
# -----------------------------------------------------------------------

@server.list_tools()
async def list_tools():
    """List available tools"""
    return [
        Tool(
            name="get_policy",
            description="Get relevant HR policy information based on a query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for in HR policies"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls"""
    if name == "get_policy":
        query = arguments.get("query", "")
        results = policy_vector_store.similarity_search(query, k=3)
        content = "\n".join([doc.page_content for doc in results])
        return [TextContent(type="text", text=content)]
    return [TextContent(type="text", text="Tool not found")]

# -----------------------------------------------------------------------
# Run the HR Policies MCP Server
# -----------------------------------------------------------------------

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())