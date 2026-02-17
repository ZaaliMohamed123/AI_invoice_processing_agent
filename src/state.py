# LangGraph State Schema for Invoice Processing Workflow.

from typing import Annotated, NotRequired
from typing_extensions import TypedDict
from operator import add


class InvoiceState(TypedDict):
    """
    Central state schema.
    """
    
    # INPUT
    pdf_path: str                          # Path to uploaded PDF file
    
    # INGEST NODE OUTPUT
    pdf_text: NotRequired[str]             # Raw text extracted from PDF
    
    # EXTRACTION NODE OUTPUT
    invoice_number: NotRequired[str]       
    vendor_name: NotRequired[str]          
    vendor_address: NotRequired[str]       
    customer_name: NotRequired[str]        
    customer_address: NotRequired[str]     
    invoice_date: NotRequired[str]         
    due_date: NotRequired[str]             
    line_items: NotRequired[list[dict]]    
    subtotal: NotRequired[float]           
    tax_rate: NotRequired[float]           
    tax_amount: NotRequired[float]         
    total: NotRequired[float]              
    currency: NotRequired[str]             
    
    # VALIDATION NODE OUTPUT
    calculations_valid: NotRequired[bool]  # True if all math checks pass
    
    # BUSINESS RULES NODE OUTPUT
    business_rules_valid: NotRequired[bool]  # True if all business rules pass
    
    #  ERRORS (Accumulating)
    # These use 'add' reducer
    errors: Annotated[list[str], add]      # List of error messages from any node
    
    # FINAL DECISION 
    # Set by: approve/reject routing
    status: NotRequired[str]               # "approved", "rejected", or "pending"
    rejection_reasons: NotRequired[list[str]]  # Why invoice was rejected
    
    # NOTIFICATION
    notification_sent: NotRequired[bool]   # True if email was sent
    notification_error: NotRequired[str]   # Error message if email failed
