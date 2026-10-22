"""Screening stub always returns manual review; it performs no screening."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Screening Demo Stub", version="0.1.0")


class ScreeningRequest(BaseModel):
    payment_reference: str = Field(pattern=r"^DEMO-[A-Z0-9-]{1,24}$")


class ScreeningResponse(BaseModel):
    payment_reference: str
    decision: Literal["manual_review_demo"]
    screened: Literal[False]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/screening/check", response_model=ScreeningResponse)
def screening_check(request: ScreeningRequest) -> ScreeningResponse:
    return ScreeningResponse(
        payment_reference=request.payment_reference,
        decision="manual_review_demo",
        screened=False,
    )
