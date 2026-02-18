"""
Gradio Web Interface for Invoice Processing Agent.
"""
import gradio as gr
import json
from src.graph import process_invoice


def format_line_items(line_items: list[dict]) -> str:
    """Format line items as a readable table."""
    if not line_items:
        return "No line items found"
    
    rows = []
    for i, item in enumerate(line_items, 1):
        rows.append(
            f"{i}. {item.get('description', 'N/A')} | "
            f"Qty: {item.get('quantity', 0)} | "
            f"Unit: ${item.get('unit_price', 0):.2f} | "
            f"Total: ${item.get('total', 0):.2f}"
        )
    return "\n".join(rows)


def format_result(result: dict) -> tuple[str, str, str, str]:
    """
    Format the processing result for display.
    
    Returns:
        Tuple of (status_html, invoice_details, line_items, errors_or_success)
    """
    status = result.get("status", "unknown")
    
    # Status with color
    if status == "approved":
        status_html = """
        <div style="padding: 20px; background-color: #d4edda; border-radius: 10px; text-align: center;">
            <h2 style="color: #155724; margin: 0;">APPROVED</h2>
            <p style="color: #155724; margin: 5px 0 0 0;">Invoice passed all validations</p>
        </div>
        """
    else:
        status_html = """
        <div style="padding: 20px; background-color: #f8d7da; border-radius: 10px; text-align: center;">
            <h2 style="color: #721c24; margin: 0;">REJECTED</h2>
            <p style="color: #721c24; margin: 5px 0 0 0;">Invoice failed validation</p>
        </div>
        """
    
    # Invoice details
    currency = result.get("currency", "USD")
    details = f"""
**Invoice Number:** {result.get('invoice_number', 'N/A')}
**Vendor:** {result.get('vendor_name', 'N/A')}
**Customer:** {result.get('customer_name', 'N/A')}
**Invoice Date:** {result.get('invoice_date', 'N/A')}
**Due Date:** {result.get('due_date', 'N/A')}

---

**Subtotal:** {currency} {result.get('subtotal', 0):,.2f}
**Tax Rate:** {(result.get('tax_rate', 0) or 0) * 100:.1f}%
**Tax Amount:** {currency} {result.get('tax_amount', 0):,.2f}
**Total:** {currency} {result.get('total', 0):,.2f}
"""
    
    # Line items
    line_items = format_line_items(result.get("line_items", []))
    
    # Errors or success message
    errors = result.get("errors", [])
    notification_sent = result.get("notification_sent", False)
    
    if errors:
        errors_text = "**Issues Found:**\n\n" + "\n".join([f"- {e}" for e in errors])
    else:
        errors_text = "**All Checks Passed**\n\nNo issues found with this invoice."
    
    if notification_sent:
        errors_text += "\n\n---\n\n*Email notification sent successfully.*"
    elif result.get("notification_error"):
        errors_text += f"\n\n---\n\n*Email notification failed: {result.get('notification_error')}*"
    
    return status_html, details, line_items, errors_text


def process_uploaded_invoice(file) -> tuple[str, str, str, str]:
    """
    Process an uploaded invoice file.
    
    Args:
        file: Uploaded file object from Gradio
        
    Returns:
        Tuple of formatted results for display
    """
    if file is None:
        return (
            "<div style='padding: 20px; background-color: #fff3cd; border-radius: 10px; text-align: center;'>"
            "<h3 style='color: #856404;'>Please upload a PDF invoice</h3></div>",
            "No file uploaded",
            "No line items",
            "Upload a PDF file to begin processing"
        )
    
    try:
        # Process the invoice through the workflow
        result = process_invoice(file.name)
        
        # Format and return results
        return format_result(result)
        
    except Exception as e:
        error_html = f"""
        <div style="padding: 20px; background-color: #f8d7da; border-radius: 10px; text-align: center;">
            <h2 style="color: #721c24; margin: 0;">ERROR</h2>
            <p style="color: #721c24; margin: 5px 0 0 0;">Processing failed</p>
        </div>
        """
        return (
            error_html,
            "Error occurred during processing",
            "N/A",
            f"**Error:** {str(e)}"
        )


# Create the Gradio interface
def create_app():
    """Create and configure the Gradio application."""
    
    with gr.Blocks(
        title="AI Invoice Processing Agent",
        theme=gr.themes.Soft(),
    ) as app:
        
        # Header
        gr.Markdown("""
        # AI Invoice Processing Agent
        
        Upload a PDF invoice to automatically extract data, validate calculations, 
        check business rules, and receive approval/rejection notification.
        
        ---
        """)
        
        with gr.Row():
            # Left column - Upload
            with gr.Column(scale=1):
                gr.Markdown("### Upload Invoice")
                file_input = gr.File(
                    label="Select PDF Invoice",
                    file_types=[".pdf"],
                    type="filepath",
                )
                process_btn = gr.Button(
                    "Process Invoice",
                    variant="primary",
                    size="lg",
                )
            
            # Right column - Status
            with gr.Column(scale=1):
                gr.Markdown("### Processing Status")
                status_output = gr.HTML(
                    value="<div style='padding: 20px; background-color: #e9ecef; border-radius: 10px; text-align: center;'>"
                    "<h3 style='color: #6c757d;'>Waiting for invoice...</h3></div>"
                )
        
        gr.Markdown("---")
        
        # Results section
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Invoice Details")
                details_output = gr.Markdown("Upload an invoice to see details")
            
            with gr.Column(scale=1):
                gr.Markdown("### Line Items")
                line_items_output = gr.Textbox(
                    label="",
                    lines=8,
                    value="Upload an invoice to see line items",
                    interactive=False,
                )
        
        gr.Markdown("---")
        
        # Validation results
        gr.Markdown("### Validation Results")
        errors_output = gr.Markdown("Upload an invoice to see validation results")
        
        # Footer
        gr.Markdown("""
        ---
        
        **Workflow:** PDF Upload → Text Extraction → LLM Data Extraction → 
        Calculation Validation → Business Rules Check → Email Notification
        
        *Built with LangChain, LangGraph, and Gradio*
        """)
        
        # Connect the button to the processing function
        process_btn.click(
            fn=process_uploaded_invoice,
            inputs=[file_input],
            outputs=[status_output, details_output, line_items_output, errors_output],
        )
    
    return app


# Main entry point
if __name__ == "__main__":
    app = create_app()
    app.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,  # Set to True to create a public link
    )
