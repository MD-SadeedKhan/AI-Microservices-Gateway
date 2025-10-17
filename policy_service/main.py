from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PolicyRequest(BaseModel):
    query: str

@app.post("/policy")
async def policy(req: PolicyRequest):
    if "forbidden" in req.query.lower():
        raise HTTPException(status_code=403, detail="Query contains forbidden word")
    return {"allowed": True}
