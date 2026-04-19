# First Quantum Minerals Operational Information System
## Technical and User Documentation Manual (Template)

Author(s):
Student Number(s):
Course:
Lecturer:
Submission Date:
Version:

---

## Document Control
| Version | Date | Author | Description of Change |
|---|---|---|---|
| 0.1 | | | Initial draft |
| 1.0 | | | Final submission |

## Table of Contents
1. Executive Summary
2. Introduction and Project Context
3. Requirements Analysis and Specification
4. System Architecture and Design Decisions
5. UML Design Artefacts
6. Implementation of Core Features
7. Error Handling and Exception Management
8. System Testing and Validation
9. User Manual
10. Technical Manual
11. Evaluation, Limitations, and Future Enhancements
12. Conclusion
13. References (APA)
14. Appendices

---

## Suggested Page Plan (Target 55-65 pages)
- Front matter: 3 pages
- Sections 1-2: 4 pages
- Section 3: 8-10 pages
- Sections 4-5: 14-18 pages
- Sections 6-7: 10-12 pages
- Section 8: 6-8 pages
- Sections 9-10: 8-10 pages
- Sections 11-12: 3-4 pages
- References + appendices: 3-5 pages

---

## 1. Executive Summary
### 1.1 Project Overview
Write a concise summary of the problem, your solution, and outcome.

### 1.2 Key Achievements
- Requirement-driven design completed
- Functional prototype implemented
- RBAC and dashboard delivered
- Testing evidence captured

### 1.3 Business Value
Explain how the system supports mining operations and decision-making.

---

## 2. Introduction and Project Context
### 2.1 Organization Background
Describe First Quantum Minerals business context.

### 2.2 Problem Statement
What operational inefficiencies are addressed by this system?

### 2.3 Project Objectives
List measurable objectives.

### 2.4 Scope
In scope:
Out of scope:

### 2.5 Stakeholders
| Stakeholder | Role | Interest | System Access |
|---|---|---|---|
| Operations Manager | | | |
| Safety Officer | | | |
| Inventory Controller | | | |

---

## 3. Requirements Analysis and Specification
### 3.1 Elicitation Approach
Describe how requirements were identified.

### 3.2 Functional Requirements
| ID | Requirement | Priority | Rationale |
|---|---|---|---|
| FR-01 | Record production logs | High | |
| FR-02 | Create and track work orders | High | |
| FR-03 | Report and manage incidents | High | |
| FR-04 | Track inventory and movements | High | |
| FR-05 | Show dashboard summary | High | |
| FR-06 | Role-based access control | High | |

### 3.3 Non-Functional Requirements
| ID | Requirement | Target |
|---|---|---|
| NFR-01 | Usability | New user can complete a task in < 3 minutes |
| NFR-02 | Availability | Local demo availability during presentation |
| NFR-03 | Performance | Typical request response < 2 seconds |
| NFR-04 | Maintainability | Layered architecture and modular code |

### 3.4 Use Case Narratives
Provide at least 4 use case narratives.

Template:
- Use Case ID:
- Use Case Name:
- Primary Actor:
- Preconditions:
- Trigger:
- Main Success Scenario:
- Alternate Flows:
- Postconditions:

### 3.5 Requirements Traceability Matrix
| Requirement ID | Design Artifact | Code Module | Test Case | Status |
|---|---|---|---|---|
| FR-01 | Use case, sequence | services/routes | TC-01 | Pass |
| FR-02 | Use case, class | services/routes | TC-02 | Pass |

---

## 4. System Architecture and Design Decisions
### 4.1 Technology Stack Justification
Explain why Python + FastAPI + SQLite + Chart.js were selected.

### 4.2 High-Level Architecture
Insert architecture diagram and explain each layer:
- Presentation (web UI)
- API layer
- Service/business layer
- Persistence layer

### 4.3 Design Principles Applied
- Separation of concerns
- Input validation
- Role-based authorization
- Error isolation and graceful feedback

### 4.4 Key Design Decisions and Trade-offs
| Decision | Options Considered | Chosen | Trade-off |
|---|---|---|---|
| Persistence | SQLite/PostgreSQL | SQLite | Fast for demo, less scalable |
| Auth model | Session/JWT | Session | Simpler local demo |

---

## 5. UML Design Artefacts
Add minimum 4 diagrams.

### 5.1 Use Case Diagram
Insert diagram image.
Explain actors and use cases.

### 5.2 Class Diagram
Insert diagram image.
Explain entities and relationships.

### 5.3 Sequence Diagram
Insert diagram image.
Suggested flow: Submit Incident or Record Inventory Movement.

### 5.4 Component or Deployment Diagram
Insert diagram image.
Explain runtime structure and dependencies.

### 5.5 Diagram Quality Notes
Explain how UML maps to implementation files.

---

## 6. Implementation of Core Features
### 6.1 Module Structure
Document folders/files and responsibilities.

### 6.2 Feature Implementation Summary
| Feature | Files | Business Rules |
|---|---|---|
| Production logging | | |
| Work orders | | |
| Incident management | | |
| Inventory management | | |
| Dashboard and graphs | | |

### 6.3 Role-Based Access Control (RBAC)
Document role permissions table.

| Action | Manager | Safety | Inventory |
|---|---|---|---|
| Record production | Yes | No | No |
| Create work order | Yes | No | No |
| Report incident | Yes | Yes | No |
| Record stock movement | Yes | No | Yes |

### 6.4 UI/UX Design Summary
Include screenshots and explain responsiveness and navigation.

---

## 7. Error Handling and Exception Management
### 7.1 Error Handling Strategy
Explain backend exceptions and frontend messages.

### 7.2 HTTP Error Mapping
| Error Scenario | HTTP Code | User-facing Message |
|---|---|---|
| Validation failure | 400 | Invalid request data |
| Not authenticated | 401 | Not logged in |
| Unauthorized role | 403 | Action not permitted |
| Missing resource | 404 | Not found |

### 7.3 Troubleshooting Guide
| Symptom | Likely Cause | Resolution |
|---|---|---|
| App not opening | Server not running | Start uvicorn command |
| Logo not visible | Static path mismatch/cache | Check /ui path, hard refresh |
| Logout not working | Stale cache/session issue | Hard refresh and re-login |

---

## 8. System Testing and Validation
### 8.1 Testing Strategy
Explain unit, functional, and manual UI tests.

### 8.2 Test Environment
- OS:
- Python version:
- Browser:
- Dependencies:

### 8.3 Test Cases
| Test ID | Scenario | Steps | Expected | Actual | Result |
|---|---|---|---|---|---|
| TC-01 | Login success | | | | |
| TC-02 | Manager creates work order | | | | |
| TC-03 | Safety blocked from work order create | | 403 | | |
| TC-04 | Inventory records stock movement | | | | |
| TC-05 | Logout invalidates session | | 401 on /auth/me | | |

### 8.4 Validation Against Requirements
Map test results to FR/NFR completion.

### 8.5 Defects and Resolutions
| Defect | Severity | Root Cause | Fix | Status |
|---|---|---|---|---|

---

## 9. User Manual
### 9.1 Getting Started
- Prerequisites
- Startup steps
- Login credentials (demo)

### 9.2 Navigation Guide
- Header and navbar
- Dashboard sections
- Data entry workflows

### 9.3 Role-specific User Instructions
- Manager workflows
- Safety workflows
- Inventory workflows

### 9.4 FAQ
Add common user questions and answers.

---

## 10. Technical Manual
### 10.1 Installation Steps
Include local setup commands.

### 10.2 Configuration
Document environment variables and defaults.

### 10.3 Runtime Commands
- Run app
- Run tests
- Debug tips

### 10.4 Codebase Overview
Summarize responsibilities of key modules.

### 10.5 Maintenance Procedures
- Updating dependencies
- Resetting demo DB
- Static asset updates

---

## 11. Evaluation, Limitations, and Future Enhancements
### 11.1 Evaluation Summary
Assess fitness for prototype purpose.

### 11.2 Current Limitations
- Prototype DB constraints
- Security hardening not fully production-ready

### 11.3 Future Enhancements
- Managed DB and cloud deployment
- Advanced analytics
- Full audit trail and approvals

---

## 12. Conclusion
Summarize project outcomes and alignment with objectives.

---

## 13. References (APA)
Use APA 7 style.

Examples:
- FastAPI. (n.d.). FastAPI documentation. https://fastapi.tiangolo.com/
- Python Software Foundation. (n.d.). Python documentation. https://docs.python.org/3/
- Chart.js. (n.d.). Chart.js documentation. https://www.chartjs.org/docs/latest/

---

## 14. Appendices
### Appendix A: Screenshots
Add labeled screenshots for each major feature.

### Appendix B: API Endpoint Catalogue
| Endpoint | Method | Purpose | Auth Required |
|---|---|---|---|

### Appendix C: Evidence Pack
- Test run outputs
- RBAC matrix output
- Error logs (if relevant)

### Appendix D: UML Source Files
Include editable files and exported images.
