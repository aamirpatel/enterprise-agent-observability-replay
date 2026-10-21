from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent.loan_support_agent import run
import json
from pathlib import Path

app = FastAPI(title="Agent Observability Starter API", version="1.0")
DATA = Path(__file__).resolve().parents[1] / "sample_data"

class AgentRequest(BaseModel):
    session_id: str
    question: str
    customer_id: str | None = None
    loan_id: str | None = None

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/agent/run")
def run_agent(request: AgentRequest):
    return run(**request.model_dump())

@app.get("/sessions")
def sessions(status: str | None = None):
    rows = [json.loads(line) for line in (DATA / "historical_sessions.jsonl").read_text().splitlines() if line]
    return [row for row in rows if not status or row["status"] == status]

@app.get("/sessions/{session_id}")
def session(session_id: str):
    sessions = [json.loads(line) for line in (DATA / "historical_sessions.jsonl").read_text().splitlines() if line]
    match = next((s for s in sessions if s["session_id"] == session_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Session not found")
    events = [json.loads(line) for line in (DATA / "trace_events.jsonl").read_text().splitlines() if line]
    match["events"] = [e for e in events if e["trace_id"] == match["trace_id"]]
    return match

@app.post("/sessions/{session_id}/replay")
def replay_placeholder(session_id: str):
    return {"session_id": session_id, "status": "not_implemented", "message": "Candidate deliverable: implement safe replay from captured inputs and approved mock dependencies."}
