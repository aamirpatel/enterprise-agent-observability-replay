# Trace Event Contract

Every observable event should include:

- `event_id`
- `trace_id`
- `parent_event_id` when applicable
- `sequence_no`
- `event_type`
- `status`
- `started_at`
- `latency_ms`
- `tool_name` for tool calls
- sanitized input and output artifacts
- error type and safe error message
- agent/model/version metadata

Do not persist secrets, raw authentication tokens, unnecessary customer data, or private hidden reasoning. Capture concise decision summaries and evidence references instead.
