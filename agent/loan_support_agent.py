"""Working deterministic Loan Support Agent supplied as a prerequisite."""
import os
import time
import uuid
import httpx

BASE_URL = os.getenv("MOCK_API_BASE_URL", "http://localhost:8001")


def _call(tool_name: str, path: str, trace_id: str):
    started = time.perf_counter()
    event = {"event_id": str(uuid.uuid4()), "trace_id": trace_id, "event_type": "tool_call", "tool_name": tool_name, "status": "started", "input": {"path": path}}
    try:
        response = httpx.get(f"{BASE_URL}{path}", timeout=3.0)
        response.raise_for_status()
        output = response.json()
        event.update(status="success", output=output, latency_ms=round((time.perf_counter() - started) * 1000, 2))
        return output, event
    except Exception as exc:
        event.update(status="failed", error_type=type(exc).__name__, error_message=str(exc), latency_ms=round((time.perf_counter() - started) * 1000, 2))
        return None, event


def run(session_id: str, question: str, customer_id: str | None = None, loan_id: str | None = None):
    trace_id = str(uuid.uuid4())
    started = time.perf_counter()
    events = [{"event_id": str(uuid.uuid4()), "trace_id": trace_id, "event_type": "agent_start", "status": "started", "input": {"question": question}}]
    lower = question.lower()

    if "loan" in lower and loan_id:
        result, event = _call("loan_status", f"/loans/{loan_id}", trace_id)
        events.append(event)
        answer = f"Loan {loan_id} is currently {result['status']}." if result else "I could not retrieve the loan status. Please try again or contact support."
    elif "kyc" in lower and customer_id:
        result, event = _call("kyc_verification", f"/kyc/{customer_id}", trace_id)
        events.append(event)
        answer = f"KYC status is {result['status']}." if result else "I could not retrieve the KYC status."
    elif "risk" in lower and customer_id:
        result, event = _call("risk_assessment", f"/risk/{customer_id}", trace_id)
        events.append(event)
        answer = f"The current risk band is {result['band']}." if result else "I could not retrieve the risk assessment."
    elif customer_id:
        result, event = _call("customer_profile", f"/customers/{customer_id}", trace_id)
        events.append(event)
        answer = f"Customer profile found for {result['name']}." if result else "I could not retrieve the customer profile."
    else:
        answer = "Please provide a customer ID or loan ID so I can use the approved banking service."

    status = "failed" if any(e.get("status") == "failed" for e in events) else "success"
    latency = round((time.perf_counter() - started) * 1000, 2)
    events.append({"event_id": str(uuid.uuid4()), "trace_id": trace_id, "event_type": "agent_end", "status": status, "output": {"answer": answer}, "latency_ms": latency})
    return {"session_id": session_id, "trace_id": trace_id, "status": status, "question": question, "answer": answer, "latency_ms": latency, "events": events}
