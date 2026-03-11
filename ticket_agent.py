# ============================================================
# ticket_agent.py — All 4 Agents + Orchestrator
# ============================================================

from datetime import datetime

class ClassifierAgent:
    def __init__(self):
        self.categories = {
            "Billing":        ["invoice", "charge", "payment", "refund", "bill", "subscription"],
            "Authentication": ["login", "password", "account", "locked", "sign in", "2fa"],
            "Performance":    ["slow", "lag", "crash", "freeze", "loading", "timeout"],
            "Data Loss":      ["missing", "deleted", "lost", "corrupt", "gone", "disappeared"],
            "Feature Request":["feature", "add", "wish", "could you", "suggestion", "would be nice"],
            "Other":          []
        }

    def classify(self, ticket_text):
        ticket_lower = ticket_text.lower()
        scores = {}
        for category, keywords in self.categories.items():
            score = sum(1 for word in keywords if word in ticket_lower)
            scores[category] = score
        best_category = max(scores, key=scores.get)
        if scores[best_category] == 0:
            best_category = "Other"
        return best_category


class PriorityAgent:
    def __init__(self):
        self.urgent_words = ["urgent", "critical", "asap", "immediately", "broken", "down", "not working", "emergency"]
        self.low_words    = ["suggestion", "minor", "eventually", "when possible", "nice to have"]

    def assess_priority(self, ticket_text, category):
        ticket_lower = ticket_text.lower()
        if any(word in ticket_lower for word in self.urgent_words) or category == "Data Loss":
            return "High"
        if any(word in ticket_lower for word in self.low_words) or category == "Feature Request":
            return "Low"
        return "Medium"


class ResolutionAgent:
    def __init__(self):
        self.solutions = {
            "Billing": (
                "We've reviewed your billing concern. Our system shows the charge is valid, "
                "but we've issued a courtesy review. You'll receive a detailed breakdown in 24 hours. "
                "If incorrect, a refund will be processed within 5-7 business days."
            ),
            "Authentication": (
                "We've detected an access issue with your account. We've sent a password reset link "
                "to your registered email. If you have 2FA enabled, use a backup code. "
                "Account will auto-unlock after 30 minutes of inactivity."
            ),
            "Performance": (
                "Our monitoring system has flagged performance issues in your region. "
                "Our engineering team is actively working on optimization. "
                "Expected resolution: 2-4 hours. We recommend clearing cache in the meantime."
            ),
            "Data Loss": (
                "URGENT: We've initiated emergency data recovery protocols. "
                "Our data team has been alerted and is working on restoration. "
                "Preliminary backup check shows data may be recoverable. ETA: 1-2 hours."
            ),
            "Feature Request": (
                "Thank you for the valuable suggestion! We've logged this as a feature request "
                "and forwarded it to our product team. We'll notify you if it's added to our roadmap."
            ),
            "Other": (
                "Thank you for reaching out. A support specialist has been assigned to your case "
                "and will respond within 24 hours with a personalized solution."
            )
        }

    def resolve(self, category):
        return self.solutions.get(category, self.solutions["Other"])


class EscalationAgent:
    """
    NEW AGENT: Decides if a ticket needs human review.
    If confidence is low or issue is too complex, escalates to human.
    This makes the system more realistic — not everything is auto-resolved.
    """
    def __init__(self):
        # These keywords signal complex issues a human should review
        self.escalation_triggers = [
            "legal", "lawsuit", "lawyer", "sue",
            "fraud", "scam", "hacked", "breach",
            "not resolved", "still broken", "second time",
            "third time", "manager", "supervisor", "complaint",
            "unacceptable", "terrible", "worst"
        ]

    def should_escalate(self, ticket_text, priority, category):
        """
        Returns True if this ticket should go to a human agent.
        Escalation logic:
        - Contains escalation trigger words
        - OR is "Other" category (we don't have a good auto-fix)
        """
        ticket_lower = ticket_text.lower()
        has_trigger  = any(word in ticket_lower for word in self.escalation_triggers)
        is_unknown   = (category == "Other")
        return has_trigger or is_unknown


class PreventionAgent:
    def __init__(self):
        self.ticket_history = {}

    def update_history(self, category):
        if category not in self.ticket_history:
            self.ticket_history[category] = 0
        self.ticket_history[category] += 1

    def get_predictions(self):
        predictions = []
        for category, count in self.ticket_history.items():
            if count >= 3:
                predictions.append({
                    "category":     category,
                    "ticket_count": count,
                    "warning": f"⚠️ High volume of '{category}' tickets ({count} tickets). "
                               f"Consider proactive outreach or a system check."
                })
        return predictions


class TicketOrchestrator:
    def __init__(self):
        self.classifier  = ClassifierAgent()
        self.prioritizer = PriorityAgent()
        self.resolver    = ResolutionAgent()
        self.escalator   = EscalationAgent()   # ← NEW
        self.preventer   = PreventionAgent()

        self.processed_tickets = []
        self.ticket_counter    = 1

        # Track resolution start time for metrics
        self.total_resolution_ms = 0

    def process_ticket(self, customer_name, ticket_text):
        start_time = datetime.now()

        category   = self.classifier.classify(ticket_text)
        priority   = self.prioritizer.assess_priority(ticket_text, category)
        escalated  = self.escalator.should_escalate(ticket_text, priority, category)
        resolution = self.resolver.resolve(category)

        self.preventer.update_history(category)

        # Calculate how long processing took (in milliseconds)
        end_time   = datetime.now()
        elapsed_ms = int((end_time - start_time).total_seconds() * 1000)
        # Add a realistic simulated processing time for demo purposes
        simulated_ms = elapsed_ms + 1200  # simulate 1.2 seconds agent thinking time
        self.total_resolution_ms += simulated_ms

        # Status depends on escalation
        status = "Escalated to Human" if escalated else "Resolved"

        ticket = {
            "id":           f"TKT-{str(self.ticket_counter).zfill(4)}",
            "customer":     customer_name,
            "text":         ticket_text,
            "category":     category,
            "priority":     priority,
            "resolution":   resolution,
            "escalated":    escalated,
            "status":       status,
            "resolution_ms": simulated_ms,
            "timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.processed_tickets.append(ticket)
        self.ticket_counter += 1
        return ticket

    def get_stats(self):
        total = len(self.processed_tickets)
        if total == 0:
            return {
                "total": 0, "high": 0, "medium": 0, "low": 0,
                "categories": {}, "prevention_alerts": [],
                "escalated": 0, "auto_resolved": 0,
                "avg_resolution_sec": 0, "cost_saved": 0,
                "auto_resolution_rate": 0
            }

        priorities    = {"High": 0, "Medium": 0, "Low": 0}
        categories    = {}
        escalated     = 0
        auto_resolved = 0

        for t in self.processed_tickets:
            priorities[t["priority"]] += 1
            cat = t["category"]
            categories[cat] = categories.get(cat, 0) + 1
            if t["escalated"]:
                escalated += 1
            else:
                auto_resolved += 1

        avg_ms  = self.total_resolution_ms / total if total > 0 else 0
        avg_sec = round(avg_ms / 1000, 1)

        # Cost calculation:
        # Industry average: $15 per human-handled ticket
        # Auto-resolved tickets save that cost
        cost_saved = auto_resolved * 15

        auto_rate = round((auto_resolved / total) * 100, 1) if total > 0 else 0

        return {
            "total":               total,
            "high":                priorities["High"],
            "medium":              priorities["Medium"],
            "low":                 priorities["Low"],
            "categories":          categories,
            "prevention_alerts":   self.preventer.get_predictions(),
            "escalated":           escalated,
            "auto_resolved":       auto_resolved,
            "avg_resolution_sec":  avg_sec,
            "cost_saved":          cost_saved,
            "auto_resolution_rate": auto_rate
        }