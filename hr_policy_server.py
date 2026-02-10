import os
from dotenv import load_dotenv
from fastmcp import FastMCP

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings

# -----------------------------------------------------------------------
# Setup the MCP Server
# -----------------------------------------------------------------------
load_dotenv()
hr_policies_mcp = FastMCP("HR-Policies-MCP-Server")

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
# Setup the MCP tool to query for policies, given a user query string
# -----------------------------------------------------------------------

@hr_policies_mcp.tool()
def get_policy(query: str) -> str:
    """Get relevant HR policy information based on a query"""
    results = policy_vector_store.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in results])

# -----------------------------------------------------------------------
# Setup the MCP prompt for the LLM
# -----------------------------------------------------------------------

@hr_policies_mcp.prompt()
def get_llm_prompt(query: str) -> str:
    """Generate a prompt for the LLM to answer HR policy questions"""
    return f"""You are an HR policy expert. Answer the following question about company HR policies based on the provided information.
    
Question: {query}

Please provide a clear and concise answer."""

# -----------------------------------------------------------------------
# Run the HR Policies MCP Server
# -----------------------------------------------------------------------

if __name__ == "__main__":
    hr_policies_mcp.run(transport="stdio", log_level="debug")