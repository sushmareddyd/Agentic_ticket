import requests
import time

SAMPLE_TICKETS = [
    {"customer_name": "Alice Johnson",  "ticket_text": "My login is broken, I can't sign in since yesterday. This is urgent!"},
    {"customer_name": "Bob Smith",      "ticket_text": "I was charged twice for my subscription this month. Please refund."},
    {"customer_name": "Carol Davis",    "ticket_text": "The app is loading very slowly and keeps timing out."},
    {"customer_name": "David Lee",      "ticket_text": "All my project files are missing! They were there yesterday. Emergency!"},
    {"customer_name": "Eva Brown",      "ticket_text": "Would be nice if you could add a dark mode feature."},
    {"customer_name": "Frank Wilson",   "ticket_text": "Password reset email is not arriving. Account is locked."},
    {"customer_name": "Grace Taylor",   "ticket_text": "Invoice shows wrong amount. I should be on the basic plan."},
    {"customer_name": "Henry Martinez", "ticket_text": "Dashboard crashes every time I try to export a report."},
    {"customer_name": "Irene Clark",    "ticket_text": "Login page keeps saying invalid credentials even though password is correct."},
    {"customer_name": "James Anderson", "ticket_text": "I'd like to suggest adding CSV export to the reports section."},
    {"customer_name": "Karen White",    "ticket_text": "System is down completely, none of our team can log in. ASAP!"},
    {"customer_name": "Leo Harris",     "ticket_text": "My data from last week seems to have disappeared from the dashboard."},
]

def seed():
    print("Seeding sample tickets...")
    for i, ticket in enumerate(SAMPLE_TICKETS):
        try:
            resp = requests.post(
                "http://localhost:5000/submit_ticket",
                json=ticket,
                headers={"Content-Type": "application/json"}
            )
            if resp.status_code == 200:
                result = resp.json()
                print(f"  [{i+1}] {result['id']} | {result['category']} | {result['priority']} | {ticket['customer_name']}")
            else:
                print(f"  [{i+1}] Error: {resp.text}")
        except Exception as e:
            print(f"  Error: {e}. Make sure app.py is running first!")
        time.sleep(0.2)
    print("\nDone! Refresh the dashboard to see all tickets.")

if __name__ == "__main__":
    seed()
