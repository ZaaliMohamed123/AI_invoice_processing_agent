"""
Ingest Node - First node in the workflow.

This node receives the PDF path from the state and extracts the text content.
It's the entry point of the processing pipeline.
"""
from src.state import InvoiceState
from src.services.pdf_service import extract_text_from_pdf, PDFExtractionError


def ingest_node(state: InvoiceState) -> dict:
    """
    Extract text from the uploaded PDF invoice.
    
    Args:
        state: Current workflow state with pdf_path set
        
    Returns:
        Dict with state updates
    """
    pdf_path = state["pdf_path"]
    
    try:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_path)
        
        # Return state update with extracted text
        return {
            "pdf_text": pdf_text
        }
        
    except PDFExtractionError as e:
        # Return error to be accumulated in state.errors
        return {
            "errors": [f"PDF Ingestion Error: {str(e)}"]
        }
    except Exception as e:
        # Catch any unexpected errors
        return {
            "errors": [f"Unexpected error during PDF ingestion: {str(e)}"]
        }
