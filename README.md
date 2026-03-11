# AgentDesk — Agentic AI Customer Support System
---

## What This System Does

AgentDesk is a **Multi-Agent AI System** that autonomously handles customer support tickets.
It classifies, prioritizes, escalates, resolves, and learns from tickets —
all without any human intervention — and displays everything on a real-time live dashboard.

---

## Problem Statement

Service tickets are a primary indicator of customer issues and operational inefficiencies.
High ticket volumes strain support teams, reduce customer satisfaction, and increase costs.
This system addresses that by:

- **Reducing** ticket load through instant AI resolution
- **Preventing** future tickets by detecting patterns and sending proactive alerts
- **Escalating** only the complex cases that truly need human attention

---

## Architecture — 5 Agents + 1 Orchestrator
```
Customer Ticket Submitted
          ↓
   [Orchestrator]          ← Controls the entire pipeline flow
          ↓
[1. Classifier Agent]      ← What type of problem is this?
          ↓
[2. Priority Agent]        ← How urgent is it? (High / Medium / Low)
          ↓
[3. Escalation Agent]      ← Should a human review this, or can AI handle it?
          ↓
[4. Resolution Agent]      ← What is the fix? Generate a response.
          ↓
[5. Prevention Agent]      ← Learn from this. Detect patterns. Raise alerts.
          ↓
   Real-Time Dashboard
```

---

## Agentic AI Concepts Demonstrated

| Concept | How It Is Implemented |
|---------|----------------------|
| **Autonomy** | Agents process tickets end-to-end without human intervention |
| **Multi-Agent System** | 5 specialized agents, each with a single responsibility |
| **Orchestration** | One orchestrator coordinates all agents in sequence |
| **Proactive Decision-Making** | Prevention Agent raises alerts before more tickets come in |
| **Conditional Routing** | Escalation Agent dynamically routes to AI or human path |
| **Self-Improvement** | System learns from ticket history to improve future prevention |
| **Real-Time Visibility** | Dashboard shows each agent firing live with activity log |

---

## Why We Did Not Use LangChain or LangGraph

LangChain and LangGraph are frameworks that wrap LLM-based agent logic.
We deliberately built our agents from scratch using pure Python because:

1. This assignment evaluates **understanding** of agentic AI — not framework usage
2. Building from scratch proves we know what these frameworks do under the hood
3. Every line of code is readable and explainable without external documentation
4. No API key or paid LLM service is required to run the prototype

| LangGraph Concept | Our Implementation |
|-------------------|--------------------|
| Agent nodes | 5 Python classes with single responsibilities |
| Graph edges | Orchestrator calling agents in sequence |
| State management | processed_tickets list in the Orchestrator |
| Conditional routing | Escalation Agent deciding AI vs Human path |
| Memory | Prevention Agent ticket_history dictionary |

In a production system, we would use LangGraph for the agent graph,
GPT-4 for dynamic classification, and RAG for knowledge-base-driven resolutions.

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | Python 3.11 | Clean, readable, beginner-friendly |
| Web Framework | Flask | Lightweight, minimal boilerplate, perfect for prototypes |
| Cross-Origin | Flask-CORS | Allows browser to talk to Flask server |
| Frontend | HTML / CSS / JavaScript | No framework needed, fully custom dashboard |
| Fonts | Google Fonts (Syne, DM Mono, Inter) | Clean professional UI typography |
| Agent Logic | Pure Python classes | Hand-coded, no LangChain or AutoGen |
| Data Storage | In-memory (Python list) | Prototype scope — PostgreSQL for production |
| Sample Data | seed_data.py script | 12 realistic customer tickets for demo |

---

## Project Structure
```
ticket_ai/
├── app.py                  ← Flask web server, connects UI to agents
├── requirements.txt        ← Python packages needed
├── seed_data.py            ← Loads 12 sample tickets for demo
├── README.md               ← This file
├── agents/
│   └── ticket_agent.py     ← All 5 agents + Orchestrator
└── templates/
    └── dashboard.html      ← Real-time dashboard UI
```

---

## The 5 Agents — Explained

### 1. Classifier Agent
Reads the ticket text and matches keywords against category lists.
Categories: Billing, Authentication, Performance, Data Loss, Feature Request, Other.
Uses keyword scoring — the category with the most keyword matches wins.

### 2. Priority Agent
Scans the ticket for urgency keywords like "urgent", "critical", "asap", "emergency".
Returns: High, Medium, or Low priority.
Data Loss tickets are always High priority regardless of keywords.

### 3. Escalation Agent (NEW)
Checks if the ticket contains complex trigger words like:
"manager", "lawsuit", "fraud", "second time", "unacceptable", "complaint".
If found → routes to Human Review.
If not found → AI handles it automatically.
This makes the system realistic — not everything should be auto-resolved.

### 4. Resolution Agent
Looks up the category and returns a pre-written professional response.
Each category has a tailored resolution message.
In production: this would use RAG to pull from a live knowledge base.

### 5. Prevention Agent
Maintains a running count of tickets by category.
When any category reaches 3 or more tickets → raises a prevention alert.
This alert tells the support team to proactively contact customers
before more tickets come in — directly reducing future ticket volume.

---

## Real-World Impact Metrics (shown on dashboard)

| Metric | What It Measures |
|--------|-----------------|
| Avg Resolution Time | How fast AI resolves a ticket (seconds vs 4 hours human average) |
| Auto-Resolution Rate | Percentage of tickets fully handled by AI |
| Escalated to Human | Count of complex cases routed to human agents |
| Auto-Resolved | Count of tickets requiring zero human involvement |
| Est. Cost Saved | Auto-resolved tickets × $15 (industry avg cost per human-handled ticket) |

Industry benchmarks this system targets:
- 25-40% reduction in agent handling time
- 15-30% reduction in ticket volume through proactive prevention
- Up to 60% of common tickets auto-resolved without human involvement

---

## How to Run

### Step 1 — Install Python
Download Python 3.11+ from python.org
During install, check "Add Python to PATH"

### Step 2 — Open in VS Code
File → Open Folder → select the ticket_ai folder

### Step 3 — Open Terminal
Press Ctrl + ` (backtick)

### Step 4 — Install packages
```
pip install -r requirements.txt
```

### Step 5 — Start the server
```
python app.py
```

### Step 6 — Open dashboard
Open browser and go to: http://localhost:5000

### Step 7 — Load sample data (for demo)
Open a second terminal and run:
```
python seed_data.py
```

---

## Demo Script (for presentation)

1. Start python app.py in Terminal 1
2. Open http://localhost:5000 in browser
3. Run python seed_data.py in Terminal 2
4. Show the dashboard — metrics, category bars, ticket table
5. Submit a live ticket to show agents firing:
   - Name: John Smith
   - Issue: My login is not working, it is urgent, I need access immediately
   - Watch all 5 agents light up in the pipeline
6. Submit an escalation ticket to show human routing:
   - Name: Angry Customer
   - Issue: This is the second time my account broke, I want to speak to a manager. Unacceptable!
   - Watch Escalation Agent turn yellow and route to Human Review
7. After 3 Authentication tickets — show Prevention Alert firing on left panel

---

## Scalability Path (Production)

| Current Prototype | Production Version |
|------------------|--------------------|
| Keyword matching classifier | Fine-tuned BERT or GPT-4 classifier |
| Template-based resolutions | RAG pipeline with live knowledge base |
| Flask synchronous server | FastAPI with async processing |
| In-memory storage | PostgreSQL persistent database |
| Manual prevention threshold | Statistical anomaly detection |
| Single server | AWS / GCP with auto-scaling |
| Polling every 3 seconds | WebSocket for true real-time updates |
| No authentication | JWT-based user authentication |

---

## Limitations (Honest Assessment)

- Classifier uses keyword matching, not a trained ML model
- Resolution messages are templates, not dynamically generated
- Data resets when server restarts (no database)
- Prevention threshold is hardcoded at 3 tickets
- No user authentication or access control

---

## Assignment Objectives Mapping

| Objective | How Satisfied |
|-----------|--------------|
| Demonstrate understanding of agentic AI concepts | 5 agents showing autonomy, orchestration, proactive decision-making |
| Design system to reduce and prevent tickets | Resolution Agent reduces load, Prevention Agent prevents future tickets |
| Functional prototype with technical proficiency | Flask server, 5 agents, live dashboard all working end-to-end |
| Real-world impact with sample data and metrics | 12 sample tickets, 5 live metrics, cost savings, category breakdown |

---
