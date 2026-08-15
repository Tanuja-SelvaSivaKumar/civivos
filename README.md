\# CivivOS



\## Autonomous RTI \& Civic Grievance Agent for India



CivivOS is an autonomous civic operations system designed to help citizens navigate bureaucratic problems in India.



Instead of treating a complaint as a one-time form submission, CivivOS turns it into a persistent, state-driven workflow:



\*\*Complaint → Classification → Legal Route → Draft → Citizen Approval → Filing → Response Monitoring → Escalation\*\*



\---



\## What CivivOS Does



CivivOS helps a citizen move from a civic problem to a structured, trackable action.



The system can:



\- understand a citizen's complaint

\- classify the issue

\- identify an appropriate government/legal route

\- generate a draft application

\- allow citizen approval before filing

\- track the case lifecycle

\- monitor response deadlines

\- detect missed deadlines

\- generate a First Appeal when escalation is required

\- maintain a timeline/audit trail of case activity



\---



\## Case Lifecycle



```text

DRAFT\_READY

&#x20;     ↓

CITIZEN\_APPROVED

&#x20;     ↓

FILED

&#x20;     ↓

WAITING\_RESPONSE

&#x20;     ↓

WATCHER

&#x20;     ↓

deadline reached

&#x20;     ↓

FIRST\_APPEAL\_REQUIRED

&#x20;     ↓

First Appeal generated
The lifecycle is implemented as a state-driven civic workflow rather than a collection of disconnected forms.

Architecture
React Frontend
      ↓
FastAPI
      ↓
Orchestrator
      ↓
Reasoning
      ↓
Drafting
      ↓
Memory / Database
Frontend

The frontend provides:

editorial landing experience
citizen dashboard
new case creation
active case tracking
lifecycle visualization
AI reasoning view
generated civic document
audit timeline
First Appeal view
multilingual interface
Backend

The FastAPI backend exposes the civic workflow and case-management APIs.

Important routes include:

POST /api/cases
GET  /api/cases/{case_id}
GET  /api/cases/{case_id}/timeline
POST /api/cases/{case_id}/approve
POST /api/cases/{case_id}/file
POST /api/cases/{case_id}/wait
POST /api/watcher/run
GET  /api/cases/{case_id}/first-appeal
Technology
Frontend
React
Vite
React Router
CSS
multilingual UI
responsive editorial interface
Backend
Python
FastAPI
SQLite
state-driven case workflow
Supported Languages

The current interface supports:

English
Tamil
Telugu
Malayalam

The language preference is persisted locally so the selected interface language remains available after refresh.

Core Design Principle

CivivOS is built around one idea:

A civic problem should have a state, a next action, and a record of what happened.

The citizen should never have to wonder:

What happened to my complaint?
Who is responsible?
What should I do next?
When does the deadline end?
What happens if the government does not respond?

CivivOS is designed to keep those answers visible.

Running Locally
Backend
cd civivos
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.app:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
Frontend
cd civivos\frontend
npm install
npm run dev

Frontend:

http://localhost:5173
Project Structure
civivos/
├── backend/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── styles/
│   │   ├── api.js
│   │   ├── i18n.jsx
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
├── data/
└── README.md
Demo Flow

A complete demonstration can follow this path:

Create Complaint
      ↓
AI Analysis
      ↓
Draft Generated
      ↓
Citizen Approval
      ↓
File
      ↓
Wait for Response
      ↓
Watcher
      ↓
Deadline Expired
      ↓
First Appeal Required
      ↓
First Appeal Generated
Status

CivivOS is an active prototype focused on demonstrating an autonomous civic workflow for RTI and grievance escalation in India.

Author

Tanuja Selva Siva Kumar

CivivOS — Civic Operations System



