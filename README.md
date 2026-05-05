# Idempotent Digital Wallet (Microservice PoC)

A lightweight Python/FastAPI microservice demonstrating core financial engineering concepts, specifically network fault tolerance and idempotency.

## The Problem it Solves
In distributed systems, if a user's network drops exactly as they send a payment, their device might retry the request. Without backend safeguards, this results in a double-charge. 

## How it Works
This API implements an Idempotency Lock. Every transfer request requires a unique transaction_id. The backend checks this ID against a registry of processed transactions in O(1) time before executing financial logic, guaranteeing that duplicate network requests are safely ignored.

## Tech Stack
* Framework: FastAPI (Python)
* Data Validation: Pydantic
* Architecture: In-Memory State Management, RESTful routing

## Getting Started

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the API
1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```
2. The API will be available at http://127.0.0.1:8000
3. Documentation (Swagger UI) is available at http://127.0.0.1:8000/docs
