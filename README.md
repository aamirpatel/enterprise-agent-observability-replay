# Enterprise Agent Observability & Replay Platform

## Banking AI Agents Hackathon Starter Repository

This starter repository provides a working Loan Support AI Agent, mock banking APIs, database schema templates, synthetic historical traces, failure scenarios, telemetry, and a basic application framework.

Participants should focus on building the **observability, investigation, replay, analytics, and dashboard platform around the agent**. They are not required to build the AI agent itself.

> All customers, identifiers, sessions, traces, and banking records in this repository are fictional and synthetic.

## Challenge

Build a platform that can answer:

- What happened during an agent execution?
- Which tools and APIs were called?
- Why did an interaction fail?
- Can the execution be replayed safely?
- Which failures are most common?
- Are quality and latency degrading over time?

## Prerequisites included

- Working rule-based Loan Support Agent
- Mock Customer Profile, Loan Status, KYC Verification, and Risk Assessment APIs
- Historical sessions and trace events
- Failure scenarios and sample API responses
- Sample telemetry records
- PostgreSQL schema template
- FastAPI starter backend
- Streamlit starter page
- Docker Compose configuration
- Seed and smoke-test scripts

## Candidate deliverables

1. End-to-end execution capture
2. Trace and artifact storage
3. Searchable historical sessions
4. Safe deterministic session replay
5. Original-versus-replay outcome comparison
6. Root-cause and failure analysis
7. Quality and latency trend analysis
8. Executive dashboard
9. Engineering dashboard
10. Documentation and tests

## Architecture

```text
User -> Loan Support Agent -> Mock Banking APIs
                 |
                 v
        Telemetry / Trace Capture
                 |
                 v
        PostgreSQL Trace Store
                 |
        +--------+---------+
        |                  |
        v                  v
 Replay Engine      Operational Analytics
        |                  |
        +--------+---------+
                 v
       Streamlit Dashboards
```

## Quick start with Docker

```bash
cp .env.example .env
docker compose up --build
```

Services:

- Starter API: `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Mock banking APIs: `http://localhost:8001/docs`
- Streamlit starter UI: `http://localhost:8501`
- PostgreSQL: `localhost:5432`

Run a sample agent request:

```bash
curl -X POST http://localhost:8000/agent/run \
  -H "Content-Type: application/json" \
  -d '{"session_id":"demo-session","question":"What is the status of loan LN-1001?","customer_id":"CUST-1001","loan_id":"LN-1001"}'
```

## Local Python start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn mock_apis.main:app --port 8001
```

In another terminal:

```bash
source .venv/bin/activate
uvicorn api.main:app --port 8000
```

In a third terminal:

```bash
source .venv/bin/activate
streamlit run dashboard/app.py
```

## Starter versus participant scope

### Already provided

- Agent and banking API behavior
- Trace event contract
- Synthetic sample records
- Schema templates
- Basic ingestion and search endpoints
- Basic session timeline page

### Participants should implement

- Production-quality trace persistence
- OpenTelemetry instrumentation/export
- Replay orchestration and safety controls
- Replay comparison and diff logic
- Failure classification and root-cause workflows
- Quality scoring and degradation detection
- Full executive and engineering dashboards
- Authentication, authorization, masking, audit, and retention controls

## Safety and governance expectations

- Never store secrets in source control.
- Mask or tokenize customer data before persistence.
- Do not expose internal reasoning or hidden chain-of-thought. Store concise decision summaries, tool events, evidence references, validation results, and operational metadata instead.
- Replay must use synthetic or approved test data by default.
- Block replay of write operations unless explicitly allow-listed and isolated.
- Log who initiated a replay and preserve the original trace.

## Repository map

```text
agent/          Working Loan Support Agent
api/            FastAPI starter backend
mock_apis/      Four mock banking API services
sample_data/    Synthetic sessions, traces, telemetry, failures, responses
database/       PostgreSQL schema and seed templates
dashboard/      Streamlit starter UI
config/         Replay policy and failure taxonomy
scripts/        Validation and database seed utilities
tests/          Starter tests
docs/           Contracts and candidate guidance
```

## License

Use within the hackathon according to your organization's policies.
