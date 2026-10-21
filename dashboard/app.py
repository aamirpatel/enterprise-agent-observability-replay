import json
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Agent Observability", layout="wide")
st.title("Enterprise Agent Observability & Replay")
st.caption("Starter interface. Build the complete operational experience during the hackathon.")

DATA = Path(__file__).resolve().parents[1] / "sample_data"
sessions = pd.DataFrame(json.loads(line) for line in (DATA / "historical_sessions.jsonl").read_text().splitlines() if line)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sessions", len(sessions))
c2.metric("Success Rate", f"{(sessions.status.eq('success').mean() * 100):.1f}%")
c3.metric("Failure Rate", f"{(sessions.status.eq('failed').mean() * 100):.1f}%")
c4.metric("Average Latency", f"{sessions.latency_ms.mean():.0f} ms")

st.subheader("Historical sessions")
status = st.selectbox("Filter by status", ["all", "success", "failed"])
filtered = sessions if status == "all" else sessions[sessions.status == status]
st.dataframe(filtered, use_container_width=True)

st.subheader("Candidate implementation areas")
st.info("Add trace waterfall, replay controls, failure drill-down, quality trends, API health, latency distributions, authorization, audit, and data masking.")
