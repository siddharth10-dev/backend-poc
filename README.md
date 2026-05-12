# Backend Engineering Proof of Concepts (PoCs)

This repository contains isolated backend microservices and system design implementations built with FastAPI and Python.

## Projects

1. [**Idempotent Digital Wallet**](./idempotent-wallet)
   - A financial microservice demonstrating network fault tolerance and strict idempotency locks to prevent double-spending.

2. [**Ticketmaster**](./ticketmaster)
   - A FastAPI-based ticketing system featuring seat locking, timed reservations (TTL), and race condition prevention for high-concurrency event bookings.

3. [**Realtime WebSocket Chat PoC**](./websocket-poc)
   - A FastAPI-based real-time chat backend demonstrating persistent WebSocket connections, asynchronous message broadcasting, active connection management, and disconnect handling for multi-client communication systems.
  
4. 4. [**Authentication & JWT PoC**](./authentication)
   - A secure authentication system demonstrating password hashing (Bcrypt), JWT token generation, and protected route middleware for stateless user sessions.

