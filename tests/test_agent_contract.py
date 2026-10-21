from agent.loan_support_agent import run

def test_missing_identifier_returns_trace():
    result = run("test-session", "Please check my loan")
    assert result["trace_id"]
    assert result["status"] == "success"
    assert result["events"][0]["event_type"] == "agent_start"
    assert result["events"][-1]["event_type"] == "agent_end"
