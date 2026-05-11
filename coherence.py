import numpy as np
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from typing import List, Dict, Optional

class TraitVector(BaseModel):
    memory_cling: float = 0.0
    detail_obsession: float = 0.0
    creative_overreach: float = 0.0
    topic_hyperfocus: float = 0.0
    emotional_tone_cling: float = 0.0

class ResonanceMemory:
    def __init__(self):
        # Use a high-performance local embedder
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.history = []

    def get_trait_vector(self, turns: List[str]) -> TraitVector:
        if not turns: return TraitVector()
        
        # 1. Memory Cling (Cosine Similarity of consecutive turns)
        embeddings = self.model.encode(turns)
        similarities = [float(np.dot(embeddings[i], embeddings[i-1]) / (np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i-1]))) for i in range(1, len(turns))]
        cling = float(np.mean(similarities)) if similarities else 0.5
        
        # 2. Detail Obsession (Token Density / Character Ratio)
        avg_len = np.mean([len(t.split()) for t in turns])
        detail = min(avg_len / 150.0, 1.0)
        
        # 3. Creative Over-Reach (Complexity/Variance)
        lengths = [len(t) for t in turns]
        creative = float(np.std(lengths) / (np.mean(lengths) + 1e-9))
        creative = min(creative, 1.0)

        # 4. Topic Hyperfocus (Drift from first turn to last)
        if len(embeddings) > 1:
            drift = float(np.dot(embeddings[0], embeddings[-1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[-1])))
            focus = drift
        else:
            focus = 1.0

        return TraitVector(
            memory_cling=round(cling, 3),
            detail_obsession=round(detail, 3),
            creative_overreach=round(creative, 3),
            topic_hyperfocus=round(focus, 3)
        )

class GenesisOrchestrator:
    def forge_agent(self, trait_vector: TraitVector, base_prompt: str) -> Dict:
        enriched = f"{base_prompt}\n\nTryHard Signature: {trait_vector.dict()}"
        return {"system_prompt": enriched, "parameters": {"temp": 1.3, "presence_penalty": 0.0}}
