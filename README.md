# SWIFT MT Payments — Azure DevOps Microservices Reference

> **Simulation only.** This is a learning/reference project. It is not a payment processor, not production-certified, not SWIFT-certified, and not approved for banking or regulatory use. It never connects to SWIFT, a bank, a payment network, or sanctions data. It does not move money or make payment decisions.
>
> Use synthetic identifiers and data only. Never add real customer PII, account numbers, credentials, keys, production messages, or live banking integrations.

This repository demonstrates an Azure DevOps YAML pipeline around three small Python microservices, a legacy AngularJS demo console, Kubernetes manifests, and Terraform for an optional Azure AKS/ACR foundation.

## Architecture

```text
AngularJS demo console
        │
        ▼
Payments API ──► Screening stub ──► Ledger stub
        │               │                 │
        └──── returns synthetic preview and demo status ────┘

Azure DevOps: lint/test → Terraform validation → container build/scan → gated deployment placeholder
```

The services are intentionally standalone examples. They do not make live network calls to each other. The payment API builds a clearly marked, incomplete MT103-like preview from synthetic input. The screening service always returns `manual_review_demo`; it performs no screening. The ledger service keeps demo entries in process memory; it is not durable, consistent, or suitable for financial records.

## Technology

- Azure DevOps Pipelines (`azure-pipelines.yml`)
- Python 3.12 and FastAPI microservices
- AngularJS 1.8 demo UI
- Docker and Kubernetes
- Terraform with AzureRM provider for AKS and ACR

**AngularJS is end-of-life.** It is included because this is an illustrative legacy-stack request; do not use it for a new production application. See the [official AngularJS notice](https://angularjs.org/).

## Run locally

Requires Python 3.12+, Docker, and (optionally) Node/npm for local UI serving.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
PYTHONPATH=services/payments:services/screening:services/ledger pytest -q
```

Run each API in a separate terminal:

```bash
PYTHONPATH=services/payments uvicorn service_payments.main:app --port 8001 --reload
PYTHONPATH=services/screening uvicorn service_screening.main:app --port 8002 --reload
PYTHONPATH=services/ledger uvicorn service_ledger.main:app --port 8003 --reload
```

Open `web/index.html` in a browser. It uses in-memory sample rows and does not call the APIs.

Example synthetic preview request:

```bash
curl -X POST http://localhost:8001/v1/payments/preview \
  -H 'Content-Type: application/json' \
  -d '{"payment_reference":"DEMO-001","amount_minor":12500,"currency":"EUR","beneficiary_country":"DE"}'
```

The response contains a sanitized placeholder preview, not a valid or transmittable SWIFT message. The `amount_minor` is fictional and no transfer is created.

## Containers

```bash
docker build -f services/payments/Dockerfile -t payments-api:demo .
docker build -f services/screening/Dockerfile -t screening-api:demo .
docker build -f services/ledger/Dockerfile -t ledger-api:demo .
docker build -f web/Dockerfile -t payments-console:demo .
```

Images run as non-root users where supported. They are examples for pipeline practice, not hardened production images.

## Azure DevOps pipeline

Import this repository into Azure Repos or connect it to GitHub in Azure DevOps, then create a pipeline from `azure-pipelines.yml`. The pipeline runs Python lint/tests, Terraform formatting/validation, builds the service and UI containers, and scans them with Trivy. It does not push images, provision Azure resources, or deploy Kubernetes workloads.

The optional `deployDemo` pipeline parameter defaults to `false`. The deployment stage is a safe placeholder that performs no rollout. If you replace it, configure an Azure DevOps Environment named `payments-demo` with required approvals/checks, restrict service connections, use workload identity federation or another approved short-lived credential flow, and add an explicit reviewed deployment implementation. Do not put secrets in YAML or variable files.

Terraform validation uses the `TerraformInstaller@1` Azure DevOps task. Install the corresponding Marketplace extension if your organization does not already provide it. No Terraform apply is performed. The AKS/ACR configuration can incur Azure costs if applied; review pricing, identity, network, policy, and security settings first.

## Kubernetes and Terraform

- `k8s/` contains a namespace, deployments, and internal ClusterIP services. It has no ingress, secrets, real image tags, or external payment integration.
- `infra/terraform/` contains an illustrative Azure resource group, ACR, and AKS cluster. It is not automatically applied by the pipeline.

## Safety limits

This repository omits SWIFT network connectivity, message authentication, ISO 20022 migration, sanctions/AML screening, fraud controls, idempotent durable processing, payment settlement, reconciliation, audit retention, key management, monitoring, disaster recovery, and regulatory/security certification. The MT103-like preview is a teaching aid and intentionally includes conspicuous placeholders. Do not use this code for production payments or real financial/customer data.

## License

MIT. See `LICENSE`.
