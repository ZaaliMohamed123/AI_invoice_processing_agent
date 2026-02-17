"""
Pydantic Models for Invoice Data Extraction.

These models are used with LangChain's structured output feature.
When we call the LLM, we pass these models and the LLM returns data
that exactly matches this structure.

Key Concepts:
- Pydantic BaseModel: Provides automatic validation and type checking
- Field(description=...): Helps the LLM understand what each field should contain
- Nested models: LineItem is used inside InvoiceData for complex structures
"""
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    """
    Represents a single line item on an invoice.
    """
    description: str = Field(
        description="Description of the product or service"
    )
    quantity: float = Field(
        description="Quantity of items (can be decimal for hours, etc.)"
    )
    unit_price: float = Field(
        description="Price per unit"
    )
    total: float = Field(
        description="Total for this line item (quantity * unit_price)"
    )


class InvoiceData(BaseModel):
    """
    Complete structured data extracted from an invoice.
    """
    # Invoice identification
    invoice_number: str = Field(
        description="Unique invoice identifier (e.g., INV-2024-001)"
    )
    
    # Vendor (seller) information
    vendor_name: str = Field(
        description="Name of the company/person issuing the invoice"
    )
    vendor_address: str | None = Field(
        default=None,
        description="Full address of the vendor"
    )
    
    # Customer (buyer) information
    customer_name: str | None = Field(
        default=None,
        description="Name of the customer being billed"
    )
    customer_address: str | None = Field(
        default=None,
        description="Full address of the customer"
    )
    
    # Dates
    invoice_date: str = Field(
        description="Date the invoice was issued (YYYY-MM-DD format)"
    )
    due_date: str | None = Field(
        default=None,
        description="Payment due date (YYYY-MM-DD format)"
    )
    
    # Line items
    line_items: list[LineItem] = Field(
        description="List of products/services on the invoice"
    )
    
    # Totals
    subtotal: float = Field(
        description="Sum of all line items before tax"
    )
    tax_rate: float | None = Field(
        default=None,
        description="Tax rate as decimal (e.g., 0.10 for 10%)"
    )
    tax_amount: float = Field(
        description="Total tax amount"
    )
    total: float = Field(
        description="Final total (subtotal + tax)"
    )
    
    # Currency
    currency: str = Field(
        default="USD",
        description="Currency code (e.g., USD, EUR, GBP)"
    )
    
    def to_state_dict(self) -> dict:
        """
        Convert to dictionary format matching InvoiceState fields.
        """
        return {
            "invoice_number": self.invoice_number,
            "vendor_name": self.vendor_name,
            "vendor_address": self.vendor_address,
            "customer_name": self.customer_name,
            "customer_address": self.customer_address,
            "invoice_date": self.invoice_date,
            "due_date": self.due_date,
            "line_items": [item.model_dump() for item in self.line_items],
            "subtotal": self.subtotal,
            "tax_rate": self.tax_rate,
            "tax_amount": self.tax_amount,
            "total": self.total,
            "currency": self.currency,
        }
