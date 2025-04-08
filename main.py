import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deep_research_wrapper import execute_deep_research
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = FastAPI(
    title="Deep Research API",
    description="Microservice to perform deep research using dzhng/deep-research",
    version="1.0.0"
)

class ResearchRequest(BaseModel):
    query: str
    breadth: int = 3
    depth: int = 2

@app.post("/research")
async def perform_research(request: ResearchRequest):
    try:
        start_time = time.time()
        result = execute_deep_research(request.query, request.breadth, request.depth)
        elapsed = time.time() - start_time
        return {
            "query": request.query,
            "breadth": request.breadth,
            "depth": request.depth,
            "elapsed_seconds": elapsed,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
