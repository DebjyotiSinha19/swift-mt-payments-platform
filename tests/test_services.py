from fastapi.testclient import TestClient

from service_ledger.main import app as ledger_app
from service_payments.main import app as payments_app
from service_screening.main import app as screening_app


def test_payment_preview_is_only_a_synthetic_preview() -> None:
    response = TestClient(payments_app).post(
        "/v1/payments/preview",
        json={
            "payment_reference": "DEMO-001",
            "amount_minor": 12500,
            "currency": "EUR",
            "beneficiary_country": "DE",
        },
    )
    assert response.status_code == 200
    assert response.json()["status"] == "preview_only"
    assert "NOT A REAL ACCOUNT" in response.json()["mt103_like_preview"]


def test_screening_stub_never_claims_to_screen() -> None:
    response = TestClient(screening_app).post(
        "/v1/screening/check", json={"payment_reference": "DEMO-002"}
    )
    assert response.status_code == 200
    assert response.json()["screened"] is False
    assert response.json()["decision"] == "manual_review_demo"


def test_ledger_stub_records_only_demo_reference() -> None:
    response = TestClient(ledger_app).post(
        "/v1/ledger/entries",
        json={"payment_reference": "DEMO-003", "event": "preview_created"},
    )
    assert response.status_code == 200
    assert response.json()["recorded"] is True
