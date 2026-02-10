from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
import json
import asyncio

#Import the HR policy Agent implementation in this wrapper
import hr_policy_agent

app = FastAPI(title="HR Policy Agent")


class PolicyQuery(BaseModel):
    prompt: str

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/query")
async def query_policy(request: PolicyQuery):
    """Query HR policy agent"""
    try:
        result = await hr_policy_agent.run_hr_policy_agent(
            prompt=request.prompt
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)