INSERT INTO sessions(session_id, trace_id, agent_version, started_at, completed_at, status, request_text, response_text, latency_ms, quality_score, failure_category)
VALUES
('SES-001','11111111-1111-4111-8111-111111111111','loan-agent-1.0','2026-10-15T09:00:00Z','2026-10-15T09:00:00.420Z','success','What is the status of loan LN-1001?','Loan LN-1001 is currently UNDER_REVIEW.',420,0.94,NULL),
('SES-002','22222222-2222-4222-8222-222222222222','loan-agent-1.0','2026-10-15T10:00:00Z','2026-10-15T10:00:03.200Z','failed','Show customer CUST-TIMEOUT','I could not retrieve the customer profile.',3200,0.42,'TOOL_TIMEOUT'),
('SES-003','33333333-3333-4333-8333-333333333333','loan-agent-1.0','2026-10-16T11:00:00Z','2026-10-16T11:00:00.610Z','failed','What is the status of loan LN-ERROR?','I could not retrieve the loan status.',610,0.51,'API_FAILURE')
ON CONFLICT DO NOTHING;
