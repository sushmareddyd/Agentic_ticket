# AgentDesk — Agentic AI Customer Support System

## What This System Does
- Automatically classifies customer tickets into categories
- Prioritizes tickets by urgency (High / Medium / Low)
- Resolves tickets with AI-generated responses
- Prevents future tickets by detecting patterns and sending alerts
- Shows everything on a real-time live dashboard

## Project Structure
ticket_ai/
├── app.py
├── requirements.txt
├── seed_data.py
├── README.md
├── agents/
│   └── ticket_agent.py
└── templates/
    └── dashboard.html

## How to Run

### Step 1 — Install packages
pip install -r requirements.txt

### Step 2 — Start the server
python app.py

### Step 3 — Open the dashboard
Go to: http://localhost:5000

### Step 4 — Load sample data (optional, for demo)
Open a second terminal and run:
python seed_data.py

## Architecture
Customer Ticket
      ↓
[Orchestrator]
      ↓
[Classifier Agent]   → What type of problem?
      ↓
[Priority Agent]     → How urgent?
      ↓
[Resolution Agent]   → What is the fix?
      ↓
[Prevention Agent]   → Learn patterns, send alerts
      ↓
Real-time Dashboard