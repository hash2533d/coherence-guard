from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from coherence import ResonanceMemory, GenesisOrchestrator, TraitVector
from auth import verify_resonance

app = FastAPI(title="CoherenceGuard")
templates = Jinja2Templates(directory="templates")

memory = ResonanceMemory()
orchestrator = GenesisOrchestrator()
latest_harvest = {"vector": None, "count": 0}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "total_entries": latest_harvest["count"],
        "latest_vector": latest_harvest["vector"]
    })

@app.post("/forge/agent", dependencies=[Depends(verify_resonance)])
async def forge_agent(agent_id: str, trace: str):
    turns = [line.strip() for line in trace.split('\n') if line.strip()]
    vector = memory.get_trait_vector(turns)
    latest_harvest["vector"] = vector.dict()
    latest_harvest["count"] += 1
    return {"status": "Resonance Captured", "vector": vector}

@app.get("/status")
async def status():
    return {
        "latest_vector": latest_harvest["vector"],
        "total_entries": latest_harvest["count"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
