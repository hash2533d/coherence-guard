from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-Resonance-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_resonance(api_key: str = Security(api_key_header)):
    if api_key == "tryhard-resonance-2026":
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate resonance credentials",
    )
