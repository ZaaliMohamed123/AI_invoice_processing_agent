"""
Notification Node - Sends email notifications about invoice processing results.
"""
from src.state import InvoiceState
from src.services.email_service import (
    send_email,
    create_approval_email,
    create_rejection_email,
    EmailError,
)


def notification_node(state: InvoiceState) -> dict:
    """
    Determine final status and send email notification.
    
    Args:
        state: Current workflow state with all validation results
        
    Returns:
        Dict with state updates
    """
    # Determine approval status
    calculations_valid = state.get("calculations_valid", False)
    business_rules_valid = state.get("business_rules_valid", False)
    errors = state.get("errors", [])
    
    # Invoice is approved only if ALL validations pass AND no errors
    is_approved = calculations_valid and business_rules_valid and len(errors) == 0
    
    # Set status
    status = "approved" if is_approved else "rejected"
    
    # Prepare result
    result = {
        "status": status,
        "notification_sent": False,
    }
    
    # Add rejection reasons if rejected
    if not is_approved:
        result["rejection_reasons"] = errors
    
    # Create and send email
    try:
        if is_approved:
            subject, body = create_approval_email(state)
        else:
            subject, body = create_rejection_email(state)
        
        send_email(subject, body)
        result["notification_sent"] = True
        
    except EmailError as e:
        result["notification_error"] = str(e)
    except Exception as e:
        result["notification_error"] = f"Unexpected error sending notification: {e}"
    
    return result
