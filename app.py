# ============================================================
# app.py — The Web Server
# Connects our AI agents to the browser dashboard.
# ============================================================

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agents.ticket_agent import TicketOrchestrator

app = Flask(__name__)
CORS(app)

orchestrator = TicketOrchestrator()

@app.route("/")
def home():
    return render_template("dashboard.html")

@app.route("/submit_ticket", methods=["POST"])
def submit_ticket():
    data          = request.get_json()
    customer_name = data.get("customer_name", "Anonymous")
    ticket_text   = data.get("ticket_text", "")

    if not ticket_text.strip():
        return jsonify({"error": "Ticket text cannot be empty"}), 400

    result = orchestrator.process_ticket(customer_name, ticket_text)
    return jsonify(result)

@app.route("/stats")
def get_stats():
    return jsonify(orchestrator.get_stats())

@app.route("/tickets")
def get_tickets():
    tickets = list(reversed(orchestrator.processed_tickets))
    return jsonify(tickets)

if __name__ == "__main__":
    print("="*50)
    print("  Agentic AI Ticket System — Starting Up")
    print("  Open your browser: http://localhost:5000")
    print("="*50)
    app.run(debug=True, port=5000)