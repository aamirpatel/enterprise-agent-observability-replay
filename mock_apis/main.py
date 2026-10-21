from fastapi import FastAPI, HTTPException
import asyncio

app = FastAPI(title="Mock Banking APIs", version="1.0")

CUSTOMERS = {
    "CUST-1001": {"customer_id": "CUST-1001", "name": "Asha Demo", "segment": "Retail", "country": "IN"},
    "CUST-1002": {"customer_id": "CUST-1002", "name": "Ravi Sample", "segment": "Premium", "country": "IN"},
}
LOANS = {
    "LN-1001": {"loan_id": "LN-1001", "customer_id": "CUST-1001", "status": "UNDER_REVIEW", "product": "Home Loan"},
    "LN-1002": {"loan_id": "LN-1002", "customer_id": "CUST-1002", "status": "APPROVED", "product": "Vehicle Loan"},
}
KYC = {"CUST-1001": {"status": "VERIFIED"}, "CUST-1002": {"status": "PENDING_DOCUMENT"}}
RISK = {"CUST-1001": {"band": "LOW", "score": 18}, "CUST-1002": {"band": "MEDIUM", "score": 46}}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/customers/{customer_id}")
def customer_profile(customer_id: str):
    if customer_id == "CUST-TIMEOUT":
        raise HTTPException(status_code=504, detail="Simulated upstream timeout")
    if customer_id not in CUSTOMERS:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CUSTOMERS[customer_id]

@app.get("/loans/{loan_id}")
def loan_status(loan_id: str):
    if loan_id == "LN-ERROR":
        raise HTTPException(status_code=503, detail="Simulated loan service outage")
    if loan_id not in LOANS:
        raise HTTPException(status_code=404, detail="Loan not found")
    return LOANS[loan_id]

@app.get("/kyc/{customer_id}")
def kyc_verification(customer_id: str):
    if customer_id not in KYC:
        raise HTTPException(status_code=404, detail="KYC record not found")
    return {"customer_id": customer_id, **KYC[customer_id]}

@app.get("/risk/{customer_id}")
async def risk_assessment(customer_id: str, delay_ms: int = 0):
    if delay_ms:
        await asyncio.sleep(min(delay_ms, 5000) / 1000)
    if customer_id not in RISK:
        raise HTTPException(status_code=404, detail="Risk record not found")
    return {"customer_id": customer_id, **RISK[customer_id]}
