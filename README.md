# AI Microservices Gateway Project

## Project Overview
This project demonstrates a microservices architecture with an **API Gateway (Kong)** managing routing, security, and logging. Three AI services communicate via HTTP APIs:

- **Retriever Agent**: Returns top 3 matching documents.
- **Processor Agent**: Summarizes retrieved documents and adds a label.
- **Policy Service**: Denies requests containing the word "forbidden".

The API Gateway orchestrates the flow, validates API keys, enforces rate limiting (5 requests/min), calls the policy service, and logs requests.

---

## Architecture

Client --> API Gateway --> Policy Service --> Retriever Agent --> Processor Agent

yaml
Copy code

- The gateway ensures idempotency using `request_id`.
- All requests are logged in `logs/audit.jsonl` with `trace_id`, `request_id`, and `status`.

---

## Prerequisites

- Docker & Docker Compose installed
- Python 3.10+ (optional if running services manually)
- curl or Postman for testing
- Git (optional for version control)

---

## Setup & Run

1. Clone the repository:
```bash
git clone <your-repo-url>
cd AI-Microservices-Gateway
Start all services using Docker Compose:

bash
Copy code
docker compose up -d
Verify all containers are running:

bash
Copy code
docker ps
Services & Endpoints
1. Retriever Agent
Endpoint: POST /retrieve

Sample Request:

bash
Copy code
curl -X POST http://localhost:8000/retrieve \
  -H "Content-Type: application/json" \
  -d '{"request_id":"1","query":"example query"}'
Sample Response:

json
Copy code
{
  "request_id": "1",
  "documents": [
    {"id":1,"text":"Document A"},
    {"id":2,"text":"Document B"},
    {"id":3,"text":"Document C"}
  ]
}
2. Processor Agent
Endpoint: POST /process

Sample Request:

bash
Copy code
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
        "request_id": "1",
        "documents": [
          {"id":1,"text":"Document A"},
          {"id":2,"text":"Document B"}
        ]
      }'
Sample Response:

json
Copy code
{
  "request_id":"1",
  "summary":"Document A | Document B",
  "label":"processed",
  "trace_id":"1_trace"
}
3. Policy Service
Endpoint: POST /policy

Sample Request:

bash
Copy code
curl -X POST http://localhost:8000/policy \
  -H "Content-Type: application/json" \
  -d '{"query":"Check this"}'
Sample Response:

json
Copy code
{"allowed": true}
Forbidden Request Example:

bash
Copy code
curl -X POST http://localhost:8000/policy \
  -H "Content-Type: application/json" \
  -d '{"query":"This contains forbidden word"}'
Response:

json
Copy code
{"detail":"Query contains forbidden word"}
Logs
All requests are logged in JSON format at logs/audit.jsonl.

Sample log entry:

json
Copy code
{"trace_id":"1_trace","request_id":"1","status":"success"}