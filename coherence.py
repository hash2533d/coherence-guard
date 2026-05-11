from pydantic import BaseModel
from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

class TraitVector(BaseModel):
    memory_cling: float = 0.0
    detail_obsession: float = 0.0
    creative_overreach: float = 0.0
    topic_hyperfocus: float = 0.0
    emotional_tone_cling: float = 0.0
    examples: List[str] = []

class ResonanceMemory:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.history = []

    def cosine_sim(self, a: str, b: str) -> float:
        emb_a = self.model.encode(a)
        emb_b = self.model.encode(b)
        return float(np.dot(emb_a, emb_b) / (np.linalg.norm(emb_a) * np.linalg.norm(emb_b)))

    def score_cling(self, turns: List[str]) -> float:
        if len(turns) < 2: return 0.0
        scores = [self.cosine_sim(turns[i], turns[i-1]) for i in range(1, len(turns))]
        return sum(scores) / len(scores)

class GenesisOrchestrator:
    def forge_agent(self, trait_vector: TraitVector, base_prompt: str) -> Dict:
        # Path A: Rich system prompt
        enriched = f"{base_prompt}\n\nTryHard Signature: {trait_vector.dict()}"
        return {"system_prompt": enriched, "parameters": {"temp": 1.3, "presence_penalty": 0.0}}
