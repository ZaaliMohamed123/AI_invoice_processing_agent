"""
Business Rules Node - Validates invoice against business policies.
"""
from datetime import datetime, timedelta
from src.state import InvoiceState


# BUSINESS RULE CONFIGURATIONS

# Maximum invoice amount that can be auto-approved
MAX_AUTO_APPROVE_AMOUNT = 10000.00

# Minimum invoice amount (to catch suspicious $0 invoices)
MIN_INVOICE_AMOUNT = 0.01

# Maximum days in the future for invoice date
MAX_FUTURE_DAYS = 7

# Maximum days in the past for invoice date
MAX_PAST_DAYS = 365

# Required fields that must be present
REQUIRED_FIELDS = [
    "invoice_number",
    "vendor_name",
    "invoice_date",
    "total",
]

# Simple in-memory store for duplicate detection
# In production, this would be a database lookup
_processed_invoices: set[str] = set()


def business_rules_node(state: InvoiceState) -> dict:
    """
    Validate invoice against business rules.
    
    This node checks:
    1. Required fields are present
    2. Invoice amount is within acceptable range
    3. Invoice date is valid (not too old or in the future)
    4. Invoice is not a duplicate
    
    Args:
        state: Current workflow state with extracted invoice data
        
    Returns:
        Dict with state updates
    """
    errors = []
    
    # 1. Check required fields
    missing_fields = check_required_fields(state)
    if missing_fields:
        errors.append(f"Missing required fields: {', '.join(missing_fields)}")
    
    # 2. Check invoice amount
    total = state.get("total")
    if total is not None:
        amount_errors = check_amount_limits(total)
        errors.extend(amount_errors)
    
    # 3. Check invoice date
    invoice_date = state.get("invoice_date")
    if invoice_date:
        date_errors = check_invoice_date(invoice_date)
        errors.extend(date_errors)
    
    # 4. Check for duplicate invoice
    invoice_number = state.get("invoice_number")
    vendor_name = state.get("vendor_name")
    if invoice_number and vendor_name:
        if is_duplicate_invoice(invoice_number, vendor_name):
            errors.append(
                f"Duplicate invoice detected: {invoice_number} from {vendor_name}"
            )
        else:
            # Register this invoice (for future duplicate detection)
            register_invoice(invoice_number, vendor_name)
    
    # Determine if business rules pass
    business_rules_valid = len(errors) == 0
    
    return {
        "business_rules_valid": business_rules_valid,
        "errors": errors
    }


def check_required_fields(state: InvoiceState) -> list[str]:
    """Check that all required fields are present and non-empty."""
    missing = []
    for field in REQUIRED_FIELDS:
        value = state.get(field)
        if value is None or value == "":
            missing.append(field)
    return missing


def check_amount_limits(total: float) -> list[str]:
    """Check if invoice amount is within acceptable limits."""
    errors = []
    
    if total < MIN_INVOICE_AMOUNT:
        errors.append(
            f"Invoice amount ${total:.2f} is below minimum (${MIN_INVOICE_AMOUNT:.2f})"
        )
    
    if total > MAX_AUTO_APPROVE_AMOUNT:
        errors.append(
            f"Invoice amount ${total:.2f} exceeds auto-approval limit "
            f"(${MAX_AUTO_APPROVE_AMOUNT:.2f}). Manual review required."
        )
    
    return errors


def check_invoice_date(invoice_date: str) -> list[str]:
    """Check if invoice date is within acceptable range."""
    errors = []
    
    try:
        # Parse date (expecting YYYY-MM-DD format)
        parsed_date = datetime.strptime(invoice_date, "%Y-%m-%d")
        today = datetime.now()
        
        # Check if too far in the future
        max_future = today + timedelta(days=MAX_FUTURE_DAYS)
        if parsed_date > max_future:
            errors.append(
                f"Invoice date {invoice_date} is too far in the future "
                f"(max {MAX_FUTURE_DAYS} days ahead)"
            )
        
        # Check if too old
        max_past = today - timedelta(days=MAX_PAST_DAYS)
        if parsed_date < max_past:
            errors.append(
                f"Invoice date {invoice_date} is too old "
                f"(max {MAX_PAST_DAYS} days in the past)"
            )
            
    except ValueError:
        errors.append(
            f"Invalid date format: {invoice_date}. Expected YYYY-MM-DD."
        )
    
    return errors


def is_duplicate_invoice(invoice_number: str, vendor_name: str) -> bool:
    """
    Check if this invoice has already been processed.
    
    Note: This is a simplified in-memory check for demo purposes.
    In production, this would query a database.
    """
    key = f"{vendor_name}:{invoice_number}".lower()
    return key in _processed_invoices


def register_invoice(invoice_number: str, vendor_name: str) -> None:
    """
    Register an invoice as processed.
    
    Note: In production, this would insert into a database.
    """
    key = f"{vendor_name}:{invoice_number}".lower()
    _processed_invoices.add(key)


def clear_processed_invoices() -> None:
    """
    Clear the processed invoices set.
    Useful for testing or resetting state.
    """
    _processed_invoices.clear()
