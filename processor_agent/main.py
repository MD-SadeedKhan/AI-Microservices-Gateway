from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()
cache = {}
LOG_FILE = "../logs/audit.jsonl"

class ProcessRequest(BaseModel):
    request_id: str
    documents: list

def log_request(trace_id, request_id, status):
    os.makedirs("../logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps({"trace_id": trace_id, "request_id": request_id, "status": status}) + "\n")

@app.post("/process")
async def process(req: ProcessRequest):
    trace_id = req.request_id + "_trace"
    if req.request_id in cache:
        log_request(trace_id, req.request_id, "cached")
        return cache[req.request_id]

    # Summarize documents (dummy logic)
    summary = " | ".join([d["text"] for d in req.documents])
    label = "processed"
    response = {"request_id": req.request_id, "summary": summary, "label": label, "trace_id": trace_id}
    cache[req.request_id] = response
    log_request(trace_id, req.request_id, "success")
    return response
