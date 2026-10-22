"""Synthetic payment preview service; it never submits a payment."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Payments Preview Service", version="0.1.0")


class PreviewRequest(BaseModel):
    payment_reference: str = Field(pattern=r"^DEMO-[A-Z0-9-]{1,24}$")
    amount_minor: int = Field(gt=0, le=100_000_000)
    currency: str = Field(pattern=r"^[A-Z]{3}$")
    beneficiary_country: str = Field(pattern=r"^[A-Z]{2}$")


class PreviewResponse(BaseModel):
    payment_reference: str
    status: Literal["preview_only"]
    message: str
    mt103_like_preview: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/payments/preview", response_model=PreviewResponse)
def payment_preview(request: PreviewRequest) -> PreviewResponse:
    """Create a sanitized display-only preview with no account/person fields."""
    amount = f"{request.amount_minor / 100:.2f}".replace(".", ",")
    preview = (
        ":20:DEMO-NOT-TRANSMIT\n"
        ":32A:00000000" + request.currency + amount + "\n"
        ":50K:/NOT-A-REAL-ACCOUNT\nSYNTHETIC SENDER\n"
        ":59:/NOT-A-REAL-ACCOUNT\nSYNTHETIC BENEFICIARY\n"
        ":70:DEMO ONLY - NOT A VALID PAYMENT INSTRUCTION"
    )
    return PreviewResponse(
        payment_reference=request.payment_reference,
        status="preview_only",
        message="No payment was created, screened, or transmitted.",
        mt103_like_preview=preview,
    )
