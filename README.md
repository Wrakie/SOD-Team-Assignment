# First Quantum Minerals - Prototype Operational Information System

This repository contains a prototype Operational Information System (OIS) designed for a large mining organization. The solution demonstrates a full mini software engineering lifecycle: requirements framing, architecture design, implementation, and verification.

## 1. Business Scope
The prototype supports selected operational processes that are common in mining operations:
- Production monitoring (daily ore processing and downtime)
- Equipment maintenance tracking (work orders)
- Safety incident reporting and closure
- Inventory stock control with low-stock alerts
- Management dashboard summary for operations leads

## 2. Technology Stack
- Python 3.11+
- FastAPI (REST API layer)
- SQLite (prototype persistence)
- Pytest (unit tests)

## 3. Architecture Overview
The system uses a layered architecture:
- `api`: HTTP endpoints and request/response contracts
- `core`: business logic and validation rules
- `db`: schema initialization and database connection helpers

This separation encourages maintainability, testability, and clear responsibilities.

## 4. Project Structure
- `docs/SRS.md`: condensed software requirements specification
- `src/mining_ois/main.py`: FastAPI app entry point
- `src/mining_ois/api/routes.py`: all REST endpoints
- `src/mining_ois/core/models.py`: Pydantic models
- `src/mining_ois/core/services.py`: service layer business logic
- `src/mining_ois/db/database.py`: database init and seed logic
- `tests/test_services.py`: service-level tests

## 5. Quick Start
### 5.1 Create a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 5.2 Install dependencies
```powershell
pip install -e .
```

### 5.3 Run the API
```powershell
uvicorn mining_ois.main:app --reload --app-dir src
```

### 5.4 Open API docs
- http://127.0.0.1:8000/docs

### 5.5 Open the operational dashboard UI
- http://127.0.0.1:8000/

### 5.6 Login for the dashboard
Use one of these demo accounts:
- `manager` / `manager123`
- `safety` / `safety123`
- `inventory` / `inventory123`

### 5.7 Where the data goes
- Browser requests go to the local FastAPI app running on `http://127.0.0.1:8000`
- The app stores records in the SQLite file `operations.db` in the project root
- The dashboard shows the same operational data that the API returns

## 6. Sample API Calls
Create a production log:
```http
POST /production-logs
{
  "site_id": 1,
  "shift_date": "2026-04-16",
  "tonnes_processed": 12650.0,
  "downtime_minutes": 45,
  "notes": "Crusher maintenance affected throughput"
}
```

Get operational summary:
```http
GET /dashboard/summary
```

## 7. Engineering Principles Demonstrated
- Modular design and separation of concerns
- Input validation through typed models
- Data integrity checks in service layer
- Repeatable initialization with schema and seed data
- Basic automated tests to reduce regression risk

## 8. Next Iteration Ideas
- Authentication and role-based access control
- Shift supervisor workflow approvals
- KPI visualizations in a web frontend
- Integration with IoT telemetry or ERP systems
