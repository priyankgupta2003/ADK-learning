"""Support ticket management system."""

from typing import Dict, Any, Optional
import json
import os
from datetime import datetime
from config import TICKETS_DIR, TICKET_STATUSES


def create_ticket(
    subject: str,
    description: str,
    priority: str = "medium",
    customer_email: Optional[str] = None
) -> str:
    """Create a new support ticket.
    
    Args:
        subject: Ticket subject
        description: Detailed description
        priority: Priority level (low, medium, high, critical)
        customer_email: Optional customer email
    """
    try:
        # Generate ticket ID
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        ticket = {
            "id": ticket_id,
            "subject": subject,
            "description": description,
            "priority": priority,
            "status": "open",
            "customer_email": customer_email,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "notes": []
        }
        
        # Save ticket
        filepath = os.path.join(TICKETS_DIR, f"{ticket_id}.json")
        with open(filepath, 'w') as f:
            json.dump(ticket, f, indent=2)
        
        return f"Support ticket {ticket_id} created successfully with {priority} priority. A team member will review it soon."
    
    except Exception as e:
        return f"Error creating ticket: {str(e)}"


def get_ticket(ticket_id: str) -> str:
    """Get information about an existing support ticket.
    
    Args:
        ticket_id: Ticket ID (format: TKT-YYYYMMDDHHMMSS)
    """
    try:
        filepath = os.path.join(TICKETS_DIR, f"{ticket_id}.json")
        
        if not os.path.exists(filepath):
            return f"Ticket {ticket_id} not found."
        
        with open(filepath, 'r') as f:
            ticket = json.load(f)
        
        result = f"Ticket {ticket_id}:\n"
        result += f"  Subject: {ticket['subject']}\n"
        result += f"  Status: {ticket['status']}\n"
        result += f"  Priority: {ticket['priority']}\n"
        result += f"  Created: {ticket['created_at']}\n"
        result += f"  Description: {ticket['description']}\n"
        
        if ticket.get('notes'):
            result += f"\n  Notes:\n"
            for note in ticket['notes']:
                result += f"    - {note['timestamp']}: {note['note']}\n"
        
        return result
    
    except Exception as e:
        return f"Error getting ticket: {str(e)}"


def update_ticket(
    ticket_id: str,
    status: Optional[str] = None,
    note: Optional[str] = None
) -> str:
    """Update a ticket's status or add notes.
    
    Args:
        ticket_id: Ticket ID
        status: New status (optional) - one of: open, in_progress, resolved, closed
        note: Note to add (optional)
    """
    try:
        filepath = os.path.join(TICKETS_DIR, f"{ticket_id}.json")
        
        if not os.path.exists(filepath):
            return f"Ticket {ticket_id} not found."
        
        with open(filepath, 'r') as f:
            ticket = json.load(f)
        
        updates = []
        
        if status and status in TICKET_STATUSES:
            ticket["status"] = status
            updates.append(f"status changed to {status}")
        
        if note:
            ticket["notes"].append({
                "timestamp": datetime.now().isoformat(),
                "note": note
            })
            updates.append("note added")
        
        ticket["updated_at"] = datetime.now().isoformat()
        
        # Save updated ticket
        with open(filepath, 'w') as f:
            json.dump(ticket, f, indent=2)
        
        if updates:
            return f"Ticket {ticket_id} updated: {', '.join(updates)}"
        else:
            return f"No updates made to ticket {ticket_id}"
    
    except Exception as e:
        return f"Error updating ticket: {str(e)}"

