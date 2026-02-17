"""
Validation Node - Validates invoice calculations.
"""
from src.state import InvoiceState


# Tolerance for floating-point comparison
TOLERANCE = 0.01


def validation_node(state: InvoiceState) -> dict:
    """
    Validate all invoice calculations.
    
    This node checks:
    1. Each line item: quantity * unit_price = total
    2. Subtotal = sum of all line item totals
    3. Tax = subtotal * tax_rate (if tax_rate provided)
    4. Total = subtotal + tax_amount
    
    Args:
        state: Current workflow state with extracted invoice data
        
    Returns:
        Dict with state updates
    """
    errors = []
    
    # Get extracted data from state
    line_items = state.get("line_items", [])
    subtotal = state.get("subtotal")
    tax_rate = state.get("tax_rate")
    tax_amount = state.get("tax_amount")
    total = state.get("total")
    
    # Check if we have the minimum required data
    if not line_items:
        errors.append("Validation Error: No line items found in invoice")
        return {
            "calculations_valid": False,
            "errors": errors
        }
    
    # 1. Validate each line item total
    calculated_subtotal = 0.0
    for i, item in enumerate(line_items, start=1):
        quantity = item.get("quantity", 0)
        unit_price = item.get("unit_price", 0)
        item_total = item.get("total", 0)
        
        expected_total = quantity * unit_price
        
        if abs(expected_total - item_total) > TOLERANCE:
            errors.append(
                f"Line item {i}: Expected total {expected_total:.2f} "
                f"(qty {quantity} x ${unit_price:.2f}), but got {item_total:.2f}"
            )
        
        calculated_subtotal += item_total
    
    # 2. Validate subtotal
    if subtotal is not None:
        if abs(calculated_subtotal - subtotal) > TOLERANCE:
            errors.append(
                f"Subtotal mismatch: Sum of line items is {calculated_subtotal:.2f}, "
                f"but subtotal shows {subtotal:.2f}"
            )
    
    # 3. Validate tax calculation (if tax_rate is provided)
    if tax_rate is not None and subtotal is not None and tax_amount is not None:
        expected_tax = subtotal * tax_rate
        if abs(expected_tax - tax_amount) > TOLERANCE:
            errors.append(
                f"Tax calculation error: Expected {expected_tax:.2f} "
                f"({subtotal:.2f} x {tax_rate*100:.1f}%), but got {tax_amount:.2f}"
            )
    
    # 4. Validate grand total
    if subtotal is not None and tax_amount is not None and total is not None:
        expected_total = subtotal + tax_amount
        if abs(expected_total - total) > TOLERANCE:
            errors.append(
                f"Total mismatch: Expected {expected_total:.2f} "
                f"(subtotal {subtotal:.2f} + tax {tax_amount:.2f}), but got {total:.2f}"
            )
    
    # Determine if calculations are valid
    calculations_valid = len(errors) == 0
    
    return {
        "calculations_valid": calculations_valid,
        "errors": errors  # Will be accumulated via the 'add' reducer
    }
