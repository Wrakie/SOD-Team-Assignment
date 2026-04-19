# Software Requirements Specification (Condensed)

## 1. Purpose
Design and implement a prototype operational information system for First Quantum Minerals that assists operational decision-making for mining sites.

## 2. Stakeholders
- Operations Manager
- Maintenance Planner
- Safety Officer
- Inventory Controller
- Site Supervisor

## 3. Functional Requirements
1. The system shall record daily production metrics for each site.
2. The system shall create and track maintenance work orders by equipment unit.
3. The system shall capture safety incidents and allow controlled closure.
4. The system shall maintain inventory item levels and stock movements.
5. The system shall identify low-stock items below reorder threshold.
6. The system shall provide a dashboard summary for open work orders, open incidents, low stock, and production totals.

## 4. Non-Functional Requirements
1. The system should support response times under 2 seconds for dashboard queries on prototype-scale data.
2. The design should separate API, business logic, and persistence concerns.
3. The codebase should be testable with automated tests for critical business rules.
4. The system should be deployable in a basic Linux or Windows environment.

## 5. Assumptions and Constraints
- Prototype implementation uses SQLite; production deployment would use enterprise RDBMS.
- Authentication is not included in this prototype phase.
- Data volume is limited to departmental usage patterns for demonstration.

## 6. Use Cases
### UC-01 Record Production Shift
- Actor: Site Supervisor
- Precondition: Valid site exists
- Main Flow: Submit date, tonnes processed, downtime, notes
- Postcondition: Production log stored and available in dashboard totals

### UC-02 Raise Maintenance Work Order
- Actor: Maintenance Planner
- Precondition: Equipment exists
- Main Flow: Enter equipment, priority, title, due date
- Postcondition: Work order appears in open maintenance list

### UC-03 Report Safety Incident
- Actor: Safety Officer
- Main Flow: Capture severity, description, lost-time indicator
- Postcondition: Incident added to open incident queue

### UC-04 Record Inventory Movement
- Actor: Inventory Controller
- Precondition: Inventory item exists
- Main Flow: Enter IN or OUT movement and quantity
- Postcondition: Current stock updates and low-stock flag recalculated

## 7. Data Entities
- Site
- Equipment
- ProductionLog
- WorkOrder
- Incident
- InventoryItem
- StockMovement

## 8. Acceptance Criteria (Prototype)
1. API endpoints are available for each core functional area.
2. Input validation rejects invalid quantities and statuses.
3. Dashboard endpoint returns coherent aggregate metrics.
4. Unit tests pass for key business rules.
