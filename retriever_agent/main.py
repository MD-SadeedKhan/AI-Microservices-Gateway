from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()
dataset = [
    {"id": 1, "text": "Document A"},
    {"id": 2, "text": "Document B"},
    {"id": 3, "text": "Document C"},
    {"id": 4, "text": "Document D"}
]
cache = {}
LOG_FILE = "../logs/audit.jsonl"

class RetrieveRequest(BaseModel):
    request_id: str
    query: str

def log_request(trace_id, request_id, status):
    os.makedirs("../logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps({"trace_id": trace_id, "request_id": request_id, "status": status}) + "\n")

@app.post("/retrieve")
async def retrieve(req: RetrieveRequest):
    trace_id = req.request_id + "_trace"
    if req.request_id in cache:
        log_request(trace_id, req.request_id, "cached")
        return cache[req.request_id]

    # Return top 3 documents (dummy logic)
    results = dataset[:3]
    response = {"request_id": req.request_id, "documents": results}
    cache[req.request_id] = response
    log_request(trace_id, req.request_id, "success")
    return response
