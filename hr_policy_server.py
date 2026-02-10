import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings

# -----------------------------------------------------------------------
# Setup the FastAPI Server
# -----------------------------------------------------------------------
load_dotenv()
app = FastAPI(title="HR-Policies-MCP-Server")

# -----------------------------------------------------------------------
# Setup the Vector Store for use in retrieving policies
# This will use the hr_policy_document.pdf file as its source
# -----------------------------------------------------------------------

pdf_filename = "hr_policy_document.pdf"
pdf_full_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), pdf_filename))

# Load and split the PDF document
try:
    loader = PyPDFLoader(pdf_full_path)
    policy_documents = loader.load_and_split()
    
    # Create embeddings
    policy_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create In memory vector store
    policy_vector_store = InMemoryVectorStore.from_documents(
        policy_documents, policy_embeddings)
except Exception as e:
    print(f"Error loading PDF: {e}")
    policy_vector_store = None

# -----------------------------------------------------------------------
# Setup the API endpoints
# -----------------------------------------------------------------------

class PolicyQuery(BaseModel):
    query: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.post("/get_policy")
async def get_policy(request: PolicyQuery):
    """Get relevant HR policy information based on a query"""
    if policy_vector_store is None:
        return {"error": "Policy database not available"}
    
    results = policy_vector_store.similarity_search(request.query, k=3)
    content = "\n".join([doc.page_content for doc in results])
    return {"policy": content}

# -----------------------------------------------------------------------
# Run the HR Policies Server
# -----------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)