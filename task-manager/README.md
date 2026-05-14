# Task Manager POC

A simple FastAPI backend proof-of-concept for managing tasks.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

- `GET /`: Welcome message
- `GET /tasks`: List all tasks
- `POST /tasks`: Create a new task
