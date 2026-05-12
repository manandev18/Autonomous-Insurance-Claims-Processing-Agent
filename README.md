# Autonomous Insurance Claims Processing Agent

An AI-powered backend system for automated FNOL (First Notice of Loss) document processing using FastAPI, Ollama, Docker, and hybrid extraction pipelines.

The system extracts insurance claim information from PDF/TXT documents, validates mandatory fields, performs semantic inference using local LLMs, classifies claims, and routes them to the appropriate workflow.

---

# Features

* PDF and TXT FNOL document processing
* Hybrid extraction architecture:

  * Deterministic regex extraction
  * Semantic inference using Ollama
* Missing field detection
* Claim classification and routing
* Explainable routing decisions
* FastAPI REST API
* Dockerized multi-container deployment
* Local LLM inference using Ollama
* Swagger API documentation

---

# Routing Rules

| Condition                                      | Route              |
| ---------------------------------------------- | ------------------ |
| Estimated damage < 25000                       | Fast-track         |
| Mandatory fields missing                       | Manual Review      |
| Description contains fraud/inconsistent/staged | Investigation Flag |
| Claim type = injury                            | Specialist Queue   |

---

# System Architecture

```text id="4w2wfx"
PDF/TXT Document
        ↓
Document Parser
        ↓
Regex Extraction
        ↓
Semantic LLM Inference (Ollama)
        ↓
Validation Engine
        ↓
Routing Engine
        ↓
Structured JSON Output
```

---

# Tech Stack

* Python
* FastAPI
* Ollama
* Phi3 Mini
* Docker
* PyMuPDF
* Regex-based extraction

---

# Project Structure

```text id="0i1hm5"
insurance-claim-agent/
│
├── app/
│   ├── main.py
│   │
│   ├── parser/
│   ├── extraction/
│   ├── routing/
│   ├── validation/
│   └── schemas/
│
├── sample_docs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Setup Instructions

## Prerequisites

Recommended:

* Docker Desktop
* 8GB RAM minimum
* Internet connection for first-time model download

---

# Step 1 — Clone Repository

```bash id="a9zbvi"
git clone <repository-url>
cd insurance-claim-agent
```

---

# Step 2 — Start Docker Containers

```bash id="e8o2uy"
docker compose up --build
```

This starts:

* FastAPI container
* Ollama container

---

# Step 3 — Pull Phi3 Mini Model

Open another terminal:

```bash id="cnol4o"
docker exec -it ollama ollama pull phi3:mini
```

The model will be downloaded locally inside the Ollama container.

Note:

* First-time setup may take several minutes.
* Model size is approximately 2–3GB.

---

# Step 4 — Restart API Container

```bash id="9mxv0l"
docker compose restart insurance-agent
```

---

# Step 5 — Open Swagger UI

```text id="mwfkr7"
http://localhost:8000/docs#/default/process_claim_process_claim_post
```

Upload:

* PDF files
* TXT files

to test the API.

---

# API Endpoint

## POST `/process-claim`

Uploads an FNOL document and returns:

* extracted fields
* missing fields
* routing decision
* reasoning

---

# Sample Output

```json id="6zrbvs"
{
  "extractedFields": {
    "policy_number": "POL777222",
    "policyholder_name": "Sarah Thompson",
    "incident_date": "09/12/2026",
    "incident_location": "Miami Downtown",
    "claimant": "suffered bodily injury and was transported to the hospital after a vehicle co",
    "asset_type": "Vehicle",
    "estimated_damage": "32000",
    "claim_type": "injury",
    "description": "Claimant suffered bodily injury and was transported to the hospital after a vehicle co Asset Details",
    "initial_estimate": {
      "value": "$32000",
      "confidence": 1,
      "inference_basis": "explicitly stated in the document"
    }
  },
  "missingFields": [],
  "recommendedRoute": "Specialist Queue",
  "reasoning": "Injury claims require specialist handling"
}
```

---

# Investigation Flag Example

If the document contains keywords such as:

* fraud
* staged
* inconsistent

the system routes the claim to:

```text id="q0eb7d"
Investigation Flag
```

---

# Specialist Queue Example

If:

```text id="j2lmql"
claim_type = injury
```

the system routes the claim to:

```text id="kg6bbo"
Specialist Queue
```

---

# Manual Review Example

If mandatory fields are missing, the system routes the claim to:

```text id="y1mzv0"
Manual Review
```

---

# Semantic Inference

The system uses Ollama-based local LLM inference to:

* infer semantic claim types
* improve extraction robustness
* handle inconsistent document formats
* support contextual understanding

Examples:

* "rear-end collision" → vehicle claim
* "hospital treatment" → injury claim
* "staged accident" → investigation flag

---

# Error Handling

The system gracefully handles:

* missing fields
* unsupported document types
* malformed PDFs
* LLM inference failures

---

# Demo Video

Demo Video Link:

```text id="km2z7t"
https://drive.google.com/file/d/1-93hN-B8HMqWMwpB9p0901n3c9NyG4ZN/view?usp=drive_link
```

---
# Important Note on LLM Responses

This project uses Ollama-based local LLM inference for semantic extraction and contextual reasoning.

Since local LLM outputs are probabilistic, extraction results may vary slightly across runs depending on:

* model behavior
* hardware constraints
* inference latency
* prompt interpretation

To improve reliability, the system combines:

* deterministic regex extraction
* validation rules
* semantic normalization
* routing logic

The architecture is designed so that core extraction and routing functionality continues to work even if LLM inference responses vary.

# Future Improvements

* OCR support for scanned PDFs
* Confidence scoring for extracted fields
* Async processing queues
* Cloud deployment
* Vector database integration
* Multi-model inference routing

---

# Author

Manan Andraskar
