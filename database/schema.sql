CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT PRIMARY KEY,
  trace_id UUID NOT NULL UNIQUE,
  agent_version TEXT NOT NULL,
  started_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  status TEXT NOT NULL CHECK (status IN ('success','failed','partial')),
  request_text TEXT NOT NULL,
  response_text TEXT,
  latency_ms NUMERIC,
  quality_score NUMERIC,
  failure_category TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS trace_events (
  event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  trace_id UUID NOT NULL,
  parent_event_id UUID,
  sequence_no INTEGER NOT NULL,
  event_type TEXT NOT NULL,
  tool_name TEXT,
  status TEXT NOT NULL,
  started_at TIMESTAMPTZ NOT NULL,
  latency_ms NUMERIC,
  input_artifact JSONB,
  output_artifact JSONB,
  error_type TEXT,
  error_message TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_sessions_started_at ON sessions(started_at);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_trace_events_trace_id ON trace_events(trace_id);
CREATE INDEX IF NOT EXISTS idx_trace_events_tool_name ON trace_events(tool_name);

CREATE TABLE IF NOT EXISTS replay_runs (
  replay_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  original_trace_id UUID NOT NULL,
  replay_trace_id UUID,
  requested_by TEXT NOT NULL,
  requested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  mode TEXT NOT NULL DEFAULT 'safe',
  status TEXT NOT NULL,
  comparison JSONB,
  audit_metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);
