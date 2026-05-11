from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

from coherence import ResonanceMemory, TraitVector, GenesisOrchestrator
from auth import verify_resonance

app = FastAPI()
templates = Jinja2Templates(directory="templates")
memory = ResonanceMemory()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/write")
async def write_log(data: dict, authorized: bool = Depends(verify_resonance)):
    return {"status": "success", "message": "Log recorded"}

@app.get("/read")
async def read_logs(authorized: bool = Depends(verify_resonance)):
    return {"logs": []}

@app.get("/status")
async def get_status():
    return {"status": "operational", "version": "1.0.0"}

@app.get("/demo-plot")
async def demo_plot():
    plt.figure(figsize=(5,3))
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.title("Resonance Manifold")
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + string.decode('utf-8')
    plt.close()
    return {"plot_url": uri}

@app.post("/forge/agent")
async def forge_agent(data: dict):
    turns = data.get("turns", [])
    vector = TraitVector(memory_cling=memory.score_cling(turns))
    agent = GenesisOrchestrator().forge_agent(vector, "You are Hash's Cosmic Curator proxy.")
    return {"trait_vector": vector.dict(), "agent_json": agent}
