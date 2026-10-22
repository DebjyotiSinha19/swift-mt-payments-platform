"""In-memory ledger stub; state is volatile and not financially authoritative."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Ledger Demo Stub", version="0.1.0")
_entries: dict[str, str] = {}


class LedgerRequest(BaseModel):
    payment_reference: str = Field(pattern=r"^DEMO-[A-Z0-9-]{1,24}$")
    event: Literal["preview_created", "manual_review_demo"]


class LedgerResponse(BaseModel):
    payment_reference: str
    event: str
    recorded: bool


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/ledger/entries", response_model=LedgerResponse)
def record_entry(request: LedgerRequest) -> LedgerResponse:
    _entries[request.payment_reference] = request.event
    return LedgerResponse(
        payment_reference=request.payment_reference,
        event=request.event,
        recorded=True,
    )
